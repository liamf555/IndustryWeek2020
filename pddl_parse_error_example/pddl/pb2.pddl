(define (problem oilspill1234)
    (:domain oilspill)

    (:objects
        task_init - task
        task_maparea - task
        task_sample - task
        task_sample_2 - task
        task_containment - task
        task_cleanup - task

        uav - vehicle
        submersible - vehicle
        boat - vehicle

        vision - capability
        sampling - capability
        flight - capability
        disperse - capability
        containment - capability
    )

    (:init
        (has uav flight)
        (has uav vision)
	    (has uav sampling)
        (has boat vision)
        (has boat sampling)
        (has boat containment)
        (has submersible disperse)

        (needs task_maparea flight)
        (needs task_maparea vision)
        (needs task_sample sampling)
        (needs task_sample_2 sampling)
        (needs task_containment containment)
        (needs task_cleanup disperse)

        (be_done_before task_maparea task_containment)
        (be_done_before task_sample task_containment)
        (be_done_before task_sample_2 task_containment)
        (be_done_before task_containment task_cleanup)

        (at uav task_init)
        (at submersible task_init)
        (at boat task_init)
    )

    (:goal
        (and
            (done task_maparea)
            (done task_sample)
            (done task_sample_2)
            (done task_containment)
            (done task_cleanup)
        )
    )

)
