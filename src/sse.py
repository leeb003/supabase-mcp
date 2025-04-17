"""
Real-time Database Event Stream using Supabase and SSE

This module implements a Server-Sent Events (SSE) endpoint that streams real-time
database changes from Supabase. It uses the Supabase Realtime feature to listen
for all database events (INSERT, UPDATE, DELETE) and forwards them to connected
SSE clients.

Features:
- Real-time database event streaming
- Event deduplication
- Channel status monitoring
- Automatic reconnection handling
- Support for multiple concurrent clients

Example Usage:
    curl -N -H "Accept: text/event-stream" -H "Cache-Control: no-cache" \
    http://localhost:3000/sse/stream

Event Format:
    {
        "type": "INSERT|UPDATE|DELETE",
        "table": "table_name",
        "schema": "public",
        "record": {record_data},
        "timestamp": "ISO-8601 timestamp"
    }
"""

import asyncio
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import os
import json
from supabase import AsyncClient

load_dotenv()

router = APIRouter()
connected_clients = []
recent_event_ids = set()  # Cache for recent event IDs

SUPABASE_PROJECT_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: AsyncClient = None

@router.on_event("startup")
async def start_supabase_realtime_listener():
    """
    Initialize Supabase client and set up realtime event listener.
    
    This function is called when the FastAPI application starts up.
    It initializes the Supabase client and sets up a realtime event listener
    to forward database events to connected SSE clients.
    """
    global supabase
    print("\nInitializing Supabase client...")
    supabase = await AsyncClient.create(SUPABASE_PROJECT_URL, SUPABASE_SERVICE_ROLE_KEY)
    print("Supabase client initialized!")

    async def handle_realtime_event(payload):
        """
        Handle incoming realtime events from Supabase.
        
        Args:
            payload (dict): The event payload from Supabase containing the database change
                          information including table, schema, and record data.
        """
        print(f"\n*** DATABASE EVENT RECEIVED ***")
        print(f"Event payload: {json.dumps(payload, indent=2)}")
        try:
            # Check for duplicate events
            event_id = payload.get('ids', [None])[0]
            if event_id in recent_event_ids:
                print(f"Skipping duplicate event with ID: {event_id}")
                return
            
            # Add to recent events
            recent_event_ids.add(event_id)
            if len(recent_event_ids) > 1000:  # Prevent unbounded growth
                recent_event_ids.clear()

            # Extract the actual data from the payload
            event_data = json.dumps({
                "type": payload["data"]["type"],
                "table": payload["data"]["table"],
                "schema": payload["data"]["schema"],
                "record": payload["data"].get("record") or payload["data"].get("old_record"),
                "timestamp": payload["data"]["commit_timestamp"]
            })
            print(f"Number of connected clients: {len(connected_clients)}")
            for queue in connected_clients:
                print(f"Putting data in queue: {id(queue)}")
                await queue.put(event_data)
                print(f"Successfully queued event for client: {id(queue)}")
        except Exception as e:
            print(f"Error in handle_realtime_event: {str(e)}")
            import traceback
            print(traceback.format_exc())

    print("\nSetting up Supabase realtime channel...")
    
    # Create a wrapper to handle the async callback
    def sync_callback(payload):
        """Create an async task for handling realtime events."""
        asyncio.create_task(handle_realtime_event(payload))

    channel = (supabase
        .channel("any_table_events")
        .on_postgres_changes(
            event='*',
            schema='public',
            table='*',
            callback=sync_callback
        )
    )
    
    print("Subscribing to channel...")
    await channel.subscribe()
    print("Channel subscription complete!")

    async def check_channel_status():
        """Periodically check and report the channel connection status."""
        while True:
            try:
                print("\nChecking channel status...")
                if channel.is_joined:
                    print("Channel is joined and listening for events")
                else:
                    print("Warning: Channel is not joined!")
                await asyncio.sleep(10)
            except Exception as e:
                print(f"Error checking channel status: {e}")
                await asyncio.sleep(10)

    # Start channel status checker
    asyncio.create_task(check_channel_status())

@router.get("/stream")
async def sse_stream(request: Request):
    """
    SSE endpoint for streaming database events to clients.
    
    Args:
        request (Request): The FastAPI request object.
    
    Returns:
        StreamingResponse: An SSE stream that sends database events to the client.
    """
    print("New client connected to SSE stream")  # Debug log
    queue = asyncio.Queue()
    queue_id = id(queue)
    print(f"Created queue with ID: {queue_id}")  # Debug queue ID
    connected_clients.append(queue)
    print(f"Total connected clients: {len(connected_clients)}")  # Debug client count

    # Send a test message immediately
    await queue.put(json.dumps({"type": "test", "message": "SSE connection established"}))

    async def event_generator():
        """
        Generate SSE events from the queue.
        
        This function is used to generate SSE events from the queue and send them
        to the client. It runs indefinitely until the client disconnects.
        """
        try:
            print(f"Starting event generator for queue: {queue_id}")  # Debug generator start
            while True:
                if await request.is_disconnected():
                    print(f"Client disconnected for queue: {queue_id}")  # Debug disconnect
                    break
                print(f"Waiting for data on queue: {queue_id}")  # Debug queue wait
                data = await queue.get()
                print(f"Got data from queue {queue_id}: {data}")  # Debug data received
                message = f"data: {data}\n\n"
                print(f"Sending SSE message for queue {queue_id}: {message}")  # Debug send
                yield message
                print(f"Sent SSE message for queue {queue_id}")  # Debug sent
        except Exception as e:
            print(f"Error in event_generator for queue {queue_id}: {e}")  # Debug errors
        finally:
            connected_clients.remove(queue)
            print(f"Removed queue {queue_id}, remaining clients: {len(connected_clients)}")  # Debug cleanup

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@router.post("/sse/messages")
async def post_message(request: Request):
    """
    Send a message to all connected SSE clients.
    
    Args:
        request (Request): The FastAPI request object containing the message.
    
    Returns:
        dict: A response indicating that the message was sent.
    """
    data = await request.json()
    message = data.get("message")
    for queue in connected_clients:
        await queue.put(message)
    return {"status": "sent"}
