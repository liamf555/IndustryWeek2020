( DEFINE ( PROBLEM OILSPILL1234 )
( :DOMAIN OILSPILL )
( :OBJECTS
	UAV SUBMERSIBLE BOAT - VEHICLE
	TASK_INIT TASK_MAPAREA TASK_SAMPLE TASK_CONTAINMENT TASK_CLEANUP TASK_FINISH - TASK
	VISION SAMPLING FLIGHT DISPERSE CONTAINMENT - CAPABILITY
)
( :INIT
	( FREE-BLOCK )
	( FREE-AGENT UAV )
	( FREE-AGENT SUBMERSIBLE )
	( FREE-AGENT BOAT )
	( IDLE UAV )
	( IDLE SUBMERSIBLE )
	( IDLE BOAT )
	( HAS UAV FLIGHT )
	( HAS UAV VISION )
	( HAS BOAT DISPERSE )
	( HAS BOAT CONTAINMENT )
	( HAS SUBMERSIBLE VISION )
	( HAS SUBMERSIBLE SAMPLING )
	( NEEDS TASK_MAPAREA FLIGHT )
	( NEEDS TASK_MAPAREA VISION )
	( NEEDS TASK_SAMPLE VISION )
	( NEEDS TASK_SAMPLE SAMPLING )
	( NEEDS TASK_CONTAINMENT DISPERSE )
	( NEEDS TASK_CONTAINMENT CONTAINMENT )
	( BE_DONE_BEFORE TASK_MAPAREA TASK_CONTAINMENT )
	( BE_DONE_BEFORE TASK_SAMPLE TASK_CONTAINMENT )
	( BE_DONE_BEFORE TASK_CONTAINMENT TASK_CLEANUP )
	( AT UAV TASK_INIT )
	( AT SUBMERSIBLE TASK_INIT )
	( AT BOAT TASK_INIT )
)
( :GOAL
	( AND
		( FREE-BLOCK )
		( DONE TASK_MAPAREA )
		( DONE TASK_SAMPLE )
		( DONE TASK_CONTAINMENT )
		( DONE TASK_CLEANUP )
		( AT UAV TASK_FINISH )
		( AT SUBMERSIBLE TASK_FINISH )
		( AT BOAT TASK_FINISH )
	)
)
)