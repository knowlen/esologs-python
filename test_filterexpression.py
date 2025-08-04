#!/usr/bin/env python3
"""
Example: Using filterExpression to efficiently fetch buff uptimes
This demonstrates how to use filter expressions to reduce API calls
when analyzing multiple buffs/debuffs.
"""

import asyncio
import os
from typing import Dict, List

from esologs import Client


async def calculate_buff_uptimes(
    events: List[Dict], start_time: float, end_time: float
) -> Dict[int, Dict[int, float]]:
    """
    Calculate buff uptimes for each player from event data.

    Returns:
        Dict mapping source_id -> ability_id -> uptime_seconds
    """
    # Track buff states: source_id -> ability_id -> apply_timestamp
    active_buffs: Dict[int, Dict[int, float]] = {}
    # Track total uptimes: source_id -> ability_id -> total_seconds
    uptimes: Dict[int, Dict[int, float]] = {}

    for event in events:
        source_id = event.get("sourceID", 0)
        ability_id = event.get("abilityGameID", 0)
        timestamp = event.get("timestamp", 0)
        event_type = event.get("type", "")

        if source_id == 0 or ability_id == 0:
            continue

        # Initialize nested dicts if needed
        if source_id not in active_buffs:
            active_buffs[source_id] = {}
            uptimes[source_id] = {}
        if ability_id not in uptimes[source_id]:
            uptimes[source_id][ability_id] = 0.0

        if event_type == "applybuff":
            # Start tracking this buff
            active_buffs[source_id][ability_id] = timestamp
        elif event_type == "removebuff":
            # Calculate duration and add to total
            if ability_id in active_buffs[source_id]:
                duration = (
                    timestamp - active_buffs[source_id][ability_id]
                ) / 1000.0  # Convert to seconds
                uptimes[source_id][ability_id] += duration
                del active_buffs[source_id][ability_id]

    # Handle any buffs still active at end of fight
    for source_id, buffs in active_buffs.items():
        for ability_id, apply_time in buffs.items():
            duration = (end_time - apply_time) / 1000.0
            uptimes[source_id][ability_id] += duration

    return uptimes


async def main():
    # Initialize client with credentials
    client_id = os.getenv("ESOLOGS_ID")
    client_secret = os.getenv("ESOLOGS_SECRET")

    if not client_id or not client_secret:
        print("Error: Please set ESOLOGS_ID and ESOLOGS_SECRET environment variables")
        return

    # Create client
    client = Client(client_id=client_id, client_secret=client_secret)

    # Example parameters from the Discord discussion
    report_code = "xb7TKHXR8DJByp4Q"
    fight_id = 17
    start_time = 2614035
    end_time = 2777081

    # Buff IDs to analyze
    # 109966 = Major Courage
    # 109967 = Minor Courage (example, actual ID may differ)
    buff_ids = [109966, 109967]
    buff_names = {109966: "Major Courage", 109967: "Minor Courage"}

    print(f"Analyzing buff uptimes for report {report_code}, fight {fight_id}")
    print(
        f"Time range: {start_time} - {end_time} ({(end_time - start_time) / 1000:.1f} seconds)"
    )
    print(f"Buffs: {', '.join(buff_names.values())}")
    print("-" * 60)

    try:
        # Method 1: Using filterExpression (efficient - single request)
        print("\nMethod 1: Using filterExpression (recommended)")
        filter_expr = f"type in ('applybuff', 'removebuff') and ability.id in ({','.join(map(str, buff_ids))})"

        response = await client.get_report_events(
            code=report_code,
            fight_i_ds=[fight_id],
            start_time=start_time,
            end_time=end_time,
            filter_expression=filter_expr,
        )

        events = response.report_data.report.events.data
        print(f"Fetched {len(events)} events in single request")

        # Calculate uptimes
        uptimes = await calculate_buff_uptimes(events, start_time, end_time)
        fight_duration = (end_time - start_time) / 1000.0

        # Display results
        print("\nBuff Uptimes by Player:")
        for source_id, buffs in uptimes.items():
            print(f"\nPlayer {source_id}:")
            for ability_id, uptime in buffs.items():
                buff_name = buff_names.get(ability_id, f"Unknown ({ability_id})")
                percentage = (uptime / fight_duration) * 100
                print(f"  {buff_name}: {uptime:.1f}s ({percentage:.1f}%)")

        # Method 2: Individual requests (less efficient - for comparison)
        print("\n" + "-" * 60)
        print("\nMethod 2: Individual ability requests (not recommended)")
        print("This method would require multiple API calls:")

        for buff_id in buff_ids:
            # We're not actually making these calls to save API quota
            # This is just to show what the less efficient approach would look like
            print(
                f"  - get_report_table(code='{report_code}', ability_id={buff_id}, ...)"
            )

        print(
            "\nNote: Method 1 is more efficient as it uses only 1 API call instead of",
            len(buff_ids),
        )

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        # Clean up
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
