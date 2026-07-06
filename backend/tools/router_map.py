"""
Maps every garminconnect.Garmin get_* method to the router it will eventually belong to.

Transcribed from the domain table in PLAN.md's Phase 9 section. Kept as a plain dict
rather than derived from the router files themselves, since those routers do not exist
yet - this phase only inventories the library.
"""

ROUTER_MAP: dict[str, str] = {
    # wellness.py
    "get_stats": "wellness.py",
    "get_user_summary": "wellness.py",
    "get_stats_and_body": "wellness.py",
    "get_body_battery": "wellness.py",
    "get_body_battery_events": "wellness.py",
    "get_all_day_stress": "wellness.py",
    "get_stress_data": "wellness.py",
    "get_heart_rates": "wellness.py",
    "get_rhr_day": "wellness.py",
    "get_respiration_data": "wellness.py",
    "get_spo2_data": "wellness.py",
    "get_hydration_data": "wellness.py",
    "get_floors": "wellness.py",
    "get_intensity_minutes_data": "wellness.py",
    "get_daily_steps": "wellness.py",
    "get_steps_data": "wellness.py",
    "get_weekly_steps": "wellness.py",
    "get_weekly_stress": "wellness.py",
    "get_weekly_intensity_minutes": "wellness.py",
    "get_all_day_events": "wellness.py",
    "get_lifestyle_logging_data": "wellness.py",
    # sleep.py
    "get_sleep_data": "sleep.py",
    "get_hrv_data": "sleep.py",
    # body.py
    "get_body_composition": "body.py",
    "get_weigh_ins": "body.py",
    "get_daily_weigh_ins": "body.py",
    "get_blood_pressure": "body.py",
    "get_fitnessage_data": "body.py",
    # activities.py
    "get_activities": "activities.py",
    "get_activities_by_date": "activities.py",
    "get_activities_fordate": "activities.py",
    "get_last_activity": "activities.py",
    "get_activity": "activities.py",
    "get_activity_details": "activities.py",
    "get_activity_splits": "activities.py",
    "get_activity_typed_splits": "activities.py",
    "get_activity_split_summaries": "activities.py",
    "get_activity_exercise_sets": "activities.py",
    "get_activity_gear": "activities.py",
    "get_activity_hr_in_timezones": "activities.py",
    "get_activity_power_in_timezones": "activities.py",
    "get_activity_weather": "activities.py",
    "get_activity_types": "activities.py",
    "get_progress_summary_between_dates": "activities.py",
    # training.py
    "get_training_status": "training.py",
    "get_training_readiness": "training.py",
    "get_morning_training_readiness": "training.py",
    "get_max_metrics": "training.py",
    "get_endurance_score": "training.py",
    "get_hill_score": "training.py",
    "get_race_predictions": "training.py",
    "get_lactate_threshold": "training.py",
    "get_cycling_ftp": "training.py",
    "get_running_tolerance": "training.py",
    "get_training_plans": "training.py",
    "get_training_plan_by_id": "training.py",
    "get_adaptive_training_plan_by_id": "training.py",
    "get_workouts": "training.py",
    "get_workout_by_id": "training.py",
    "get_scheduled_workouts": "training.py",
    "get_scheduled_workout_by_id": "training.py",
    "get_personal_record": "training.py",
    "get_goals": "training.py",
    # devices.py
    "get_devices": "devices.py",
    "get_device_last_used": "devices.py",
    "get_device_settings": "devices.py",
    "get_device_alarms": "devices.py",
    "get_device_solar_data": "devices.py",
    "get_primary_training_device": "devices.py",
    "get_unit_system": "devices.py",
    # gear.py
    "get_gear": "gear.py",
    "get_gear_defaults": "gear.py",
    "get_gear_stats": "gear.py",
    "get_gear_activities": "gear.py",
    # profile.py
    "get_full_name": "profile.py",
    "get_user_profile": "profile.py",
    "get_userprofile_settings": "profile.py",
    # badges.py
    "get_earned_badges": "badges.py",
    "get_available_badges": "badges.py",
    "get_in_progress_badges": "badges.py",
    "get_badge_challenges": "badges.py",
    "get_available_badge_challenges": "badges.py",
    "get_non_completed_badge_challenges": "badges.py",
    "get_adhoc_challenges": "badges.py",
    "get_inprogress_virtual_challenges": "badges.py",
    # nutrition.py
    "get_nutrition_daily_food_log": "nutrition.py",
    "get_nutrition_daily_meals": "nutrition.py",
    "get_nutrition_daily_settings": "nutrition.py",
    # golf.py
    "get_golf_summary": "golf.py",
    "get_golf_scorecard": "golf.py",
    "get_golf_shot_data": "golf.py",
    # womens_health.py
    "get_menstrual_data_for_date": "womens_health.py",
    "get_menstrual_calendar_data": "womens_health.py",
    "get_pregnancy_summary": "womens_health.py",
}

# Router files in the order they should appear in the generated report, matching PLAN.md's table.
ROUTER_ORDER: list[str] = [
    "wellness.py",
    "sleep.py",
    "body.py",
    "activities.py",
    "training.py",
    "devices.py",
    "gear.py",
    "profile.py",
    "badges.py",
    "nutrition.py",
    "golf.py",
    "womens_health.py",
]

ALL_METHODS: list[str] = sorted(ROUTER_MAP)
