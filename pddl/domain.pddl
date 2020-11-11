(define (domain oilspill)

    (:requirements :strips :typing :multi-agent :unfactored-privacy :EQUALITY :NEGATIVE-PRECONDITIONS :CONDITIONAL-EFFECTS :UNIVERSAL-PRECONDITIONS :DISJUNCTIVE-PRECONDITIONS)

    (:types
        vehicle task capability - object
    )

    (:predicates
        (has ?v - vehicle ?c - capability) ;; vehicles has a capability
        (needs ?t - task ?c - capability) ;; task needs a capability
        (at ?v - vehicle ?t - task) ;; vehicle at a particular task
        ;;(idle ?v - vehicle) ;; vehicle is idle
        (be_done_before ?t1 - task ?t2 - task) ;; t1 must be done before t2
        (done ?t - task) ;; task is done
    )


    (:action do-task
        :agent ?vehicle - vehicle
        :parameters (?task - task)
        :precondition ( and
            (at ?vehicle ?task)
            (FORALL (?cap - capability)
                (or ;; imply
                    (not (needs ?task ?cap))
                    (has ?vehicle ?cap)
                )
            )
            (FORALL (?othertask - task)
                (or ;; imply
                    (not (be_done_before ?othertask ?task))
                    (done ?othertask)
                )
            )
        )
        :effect (and
            (done ?task)
        )
    )

    (:action move-to-task
        :agent ?vehicle - vehicle
        :parameters (?fromtask - task ?totask - task)
        :precondition (and
            (at ?vehicle ?fromtask)
        )
        :effect (and
            (not (at ?vehicle ?fromtask))
            (at ?vehicle ?totask)
        )
    )

)