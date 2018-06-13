from Grammar.actions import NonTerminals as NT, Terminals as T
from Grammar.tree import Node, Leaf


# ================================================================
# ======================= Everquest Quests =======================
# ================================================================

cure = Node(NT.quest, 5,
            Node(NT.protection, 2,
                 Node(NT.get, 4,
                      Node(NT.goto, 3,
                           Node(NT.learn, 1,
                                Leaf(T.null)),
                           Leaf(T.goto)),
                      Node(NT.get, 4,
                           Node(NT.goto, 3,
                                Node(NT.learn, 4,
                                     Node(NT.get, 3,
                                          Node(NT.goto, 3,
                                               Node(NT.learn, 1,
                                                    Leaf(T.null)),
                                               Leaf(T.goto)),
                                          Leaf(T.gather)),
                                     Node(NT.sub_quest, 1,
                                          Node(NT.goto, 3,
                                               Node(NT.learn, 1,
                                                    Leaf(T.null)),
                                               Leaf(T.goto))),
                                     Leaf(T.give),
                                     Leaf(T.listen)),
                                Leaf(T.goto)),
                           Node(NT.get, 2,
                                Node(NT.steal, 2,
                                     Node(NT.goto, 1,
                                          Leaf(T.null)),
                                     Node(NT.kill, 1,
                                          Node(NT.goto, 1,
                                               Leaf(T.null)),
                                          Leaf(T.kill)),
                                     Leaf(T.take)
                                     )),
                           Node(NT.sub_quest, 1,
                                Node(NT.goto, 1,
                                     Leaf(T.null))),
                           Node(NT.goto, 3,
                                Node(NT.learn, 1,
                                     Leaf(T.null)),
                                Leaf(T.goto)),
                           Leaf(T.exchange)),
                      Node(NT.sub_quest, 1,
                           Node(NT.goto, 1,
                                Leaf(T.null))),
                      Node(NT.goto, 3,
                           Node(NT.learn, 1,
                                Leaf(T.null)),
                           Leaf(T.goto)),
                      Leaf(T.exchange)),
                 Node(NT.goto, 3,
                      Node(NT.learn, 1,
                           Leaf(T.null)),
                      Leaf(T.goto)),
                 Leaf(T.use)))

spy = Node(NT.quest, 1,
           Node(NT.knowledge, 2,
                Node(NT.spy, 1,
                     Node(NT.goto, 3,
                          Node(NT.learn, 3,
                               Node(NT.goto, 3,
                                    Node(NT.learn, 2,
                                         Node(NT.goto, 3,
                                              Node(NT.learn, 2,
                                                   Node(NT.goto, 3,
                                                        Node(NT.learn, 2,
                                                             Node(NT.goto, 3,
                                                                  Node(NT.learn, 1,
                                                                       Leaf(T.null)),
                                                                  Leaf(T.goto)),
                                                             Node(NT.sub_quest, 1,
                                                                  Node(NT.goto, 1,
                                                                       Leaf(T.null))),
                                                             Leaf(T.listen)),
                                                        Leaf(T.goto)),
                                                   Node(NT.sub_quest, 1,
                                                        Node(NT.goto, 1,
                                                             Leaf(T.null))),
                                                   Leaf(T.listen)),
                                              Leaf(T.goto)),
                                         Node(NT.sub_quest, 1,
                                              Node(NT.goto, 1,
                                                   Leaf(T.null))),
                                         Leaf(T.listen)),
                                    Leaf(T.goto)),
                               Node(NT.get, 4,
                                    Node(NT.goto, 3,
                                         Node(NT.learn, 1,
                                              Leaf(T.null)),
                                         Leaf(T.goto)),
                                    Node(NT.get, 1,
                                         Leaf(T.null)),
                                    Node(NT.sub_quest, 1,
                                         Node(NT.goto, 1,
                                              Leaf(T.null))),
                                    Node(NT.goto, 3,
                                         Node(NT.learn, 1,
                                              Leaf(T.null)),
                                         Leaf(T.goto)),
                                    Leaf(T.exchange)
                                    ),
                               Leaf(T.read)),
                          Leaf(T.goto)),
                     Leaf(T.spy),
                     Node(NT.goto, 3,
                          Node(NT.learn, 1,
                               Leaf(T.null)),
                          Leaf(T.goto)),
                     Leaf(T.report))))

# ================================================================
# ======================= Arbitrary Quests =======================
# ================================================================

arbitrary_quest1 = Node(NT.quest, 1,
                        Node(NT.knowledge, 3,
                             Node(NT.goto, 3,
                                  Node(NT.learn, 3,
                                       Node(NT.goto, 1,
                                            Leaf(T.null)),
                                       Node(NT.get, 2,
                                            Node(NT.steal, 1,
                                                 Node(NT.goto, 2,
                                                      Leaf(T.explore)),
                                                 Leaf(T.stealth),
                                                 Leaf(T.take))),
                                       Leaf(T.read)),
                                  Leaf(T.goto)),
                             Leaf(T.listen),
                             Node(NT.goto, 1,
                                  Leaf(T.null)),
                             Leaf(T.report)))

arbitrary_quest2 = Node(NT.steal, 1,
                        Node(NT.goto, 3,
                             Node(NT.learn, 1,
                                  Leaf(T.null)),
                             Leaf(T.goto)),
                        Leaf(T.stealth),
                        Leaf(T.take))

arbitrary_quest3 = Node(NT.quest, 9,
                        Node(NT.equipment, 3,
                             Node(NT.steal, 1,
                                  Node(NT.goto, 3,
                                       Node(NT.learn, 1,
                                            Leaf(T.null)),
                                       Leaf(T.goto)),
                                  Leaf(T.stealth),
                                  Leaf(T.take))))

tiny_goto = Node(NT.goto, 1,
                 Leaf(T.null))

small_goto = Node(NT.goto, 3,
                  Node(NT.learn, 1,
                       Leaf(T.null)),
                  Leaf(T.goto))