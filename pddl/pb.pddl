(define (problem oilspill1234)
    (:domain oilspill)

    (:objects
        task_init - task
        task_maparea - task
        task_sample - task
        task_containment - task
        task_cleanup - task
        task_finish - task

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
        (idle uav)
        (idle submersible)
        (idle boat)

        (has uav flight)
        (has uav vision)
        (has boat disperse)
        (has boat containment)
        (has submersible vision)
        (has submersible sampling)

        (needs task_maparea flight)
        (needs task_maparea vision)
        (needs task_sample vision)
        (needs task_sample sampling)
        (needs task_containment disperse)
        (needs task_containment containment)

        ;; (be_done_before task_maparea task_containment)
        ;; (be_done_before task_sample task_containment)
        ;; (be_done_before task_containment task_cleanup)
        ;; (be_done_before task_cleanup task_finish)

        (at uav task_init)
        (at submersible task_init)
        (at boat task_init)
    )

    (:goal
        (and
            (done task_maparea)
            (done task_sample)
            (done task_containment)
            (done task_cleanup)
            (at uav task_finish)
            (at submersible task_finish)
            (at boat task_finish)
        )
    )

)