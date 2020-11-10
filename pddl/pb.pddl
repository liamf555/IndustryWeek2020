(define (problem oilspill1234)
    (:domain oilspill)

    (:objects
        task_maparea - task
        task_sample - task
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
        (idle uav)
        (idle submersible)
        (idle boat)

        (has uav flight)
        (has uav vision)
        (has boat disperse)
        (has submersible vision)
        (has submersible sampling)

        (need task_maparea vision)
        (need task_sample vision)
        (need task_sample sampling)
        (need task_containment disperse)
        (need task_containment containment)

        (available task_maparea)
        (available task_sample)

        (be_done_before task_maparea task_containment)
        (be_done_before task_sample task_containment)
        (be_done_before task_containment task_cleanup)
    )

    (:goal
        (done task_maparea)
        (done task_sample)
        (done task_containment)
        (done task_cleanup)
    )

)