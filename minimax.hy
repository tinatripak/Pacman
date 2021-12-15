(import [random[randint]]
[copy[copy]])

(setv map [])
(setv coins [])
(setv pacman [0 2])
(setv ghost [3 2])
(setv size 5)
(setv walls [])
(setv massneighbours [])


(for [x (range size)]
(do 
	(setv wall [])
    (wall.append (randint 0 (- size 1)))
    (wall.append (randint 0 (- size 1)))
    (walls.append wall)))
(print "Стіни: " walls)


(for [x (range size)]
(do
  (setv tempArray [])
  (for [y (range size)]
    (do
    (setv point [])
    (point.append x)
    (point.append y)
    (if (and (in point walls) (and (!= point ghost) (!= point pacman)))
      (tempArray.append 1) 
        (do
        (tempArray.append 0)
        (coins.append point)
        ))))
  (map.append tempArray)))
(print "Їжа: " coins)
(print "Карта: " map)


(defn findWay[point [parent None]]
  (do
  (setv neighbours [[0 1] [0 -1] [1 0] [-1 0]])
  (setv freeWay [])
  (for [neighbour neighbours]
    (do
    (setv x (get neighbour 0))
    (setv y (get neighbour 1))
    (setv neighbour [])
    (neighbour.append (%(+(get point 0) x)size))
    (neighbour.append (%(+(get point 1) y)size))
    (if (is parent None)
    (neighbour.append (copy neighbour))
    (neighbour.append parent)
    )
    (if (!= 1 (get map (get neighbour 0) (get neighbour 1)))
    (freeWay.append neighbour))))
  freeWay))

(print "Знайти сусдів привідяшек :" (findWay [3 2]))
(print "Знайти сусідів пакмена :" (findWay [0 2]))
  
  
(defn ghostTurn[ghostPoint pacmanPoint](
  do
  (setv pacmanPointX (get pacmanPoint 0))
  (setv pacmanPointY (get pacmanPoint 1))
  (setv visited [])
  (visited.append ghostPoint)
  (setv nextMove (findWay ghostPoint))
  (while (!= 0 (len nextMove))
    (do
    (setv nodesToVisit nextMove)
    (setv nextMove [])
    (for [node nodesToVisit]
      (do
      (setv nodeX (get node 0))
      (setv nodeY (get node 1))
      (setv nodeNoParent [])
      (nodeNoParent.append nodeX)
      (nodeNoParent.append nodeY)
      (if (not (in nodeNoParent visited))
        (do
        (visited.append nodeNoParent)
        (if (and (= pacmanPointX nodeX  (= pacmanPointY nodeY)))
        (return (get node 2))
        )
        (+= nextMove (findWay node (get node 2)))))))))
  (get (findWay ghostPoint) 0)))


(defn maxTurn[deep pacmanPoint ghostPoint score]
  (do
  (if (or (= 0 (len coins))(= deep 0))
    (
      return score
    )
   )
  (setv freeWay (findWay pacman))
  (setv scores [])
  (for [direction freeWay](
    do
    (setv shortest (cut direction 0 2))
    (setv temp_score score)
    (setv removed_coin None)
    (if (in shortest coins)(
      do
      (setv temp_score (+ temp_score 1))
      (coins.remove shortest)
      (setv removed_coin shortest)
    ))
    ; add coins remove

    (if (= ghostPoint shortest)(
      scores.append (float "-inf")
    ) (
      do
      (scores.append (+ "вітка: " (str(minTurn (- deep 1) shortest ghostPoint temp_score))))
    ))
    (if (not(is removed_coin None))(
      coins.append shortest
    ))
  ))
  scores
))

(defn minTurn[deep pacmanPoint ghostPoint score]
  (do
  (setv ghost (cut (ghostTurn ghostPoint pacmanPoint) 0 2))
  (if (= ghost pacmanPoint)
    (return (float "-inf"))
  (return (maxTurn deep pacmanPoint ghost score)))))


(print "Зробити поворот привідяшки (3,2):" (ghostTurn ghost pacman))

(defn pacmanAction[]
(
  maxTurn 2 pacman ghost 0
))

(print "Дерево з глибиною 2:" (pacmanAction ))