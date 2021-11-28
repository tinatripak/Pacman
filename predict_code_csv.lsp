(ql:quickload :fare-csv)
(ql:quickload "iterate")
(use-package :iterate)

(defvar maxScore 100)

(defvar data
  (fare-csv:read-csv-file #P"C:/Users/Кристина/PycharmProjects/pacman/results.csv"))

(defun parseThreeColumns (it)
  (list (parse-integer (second it)) (read-from-string (third it))(parse-integer (fourth it))))

(defvar workData
  (map 'list (lambda (it) (parseThreeColumns it)) (cdr data)))

(print workdata)

(defun average (ns)
  (/ (apply '+ ns) (float (length ns))))

(defvar scoreMean (average (map 'list
                              (lambda (it) (first it))
                              workdata)))

(defvar timeMean (average (map 'list
                              (lambda (it) (second it))
                              workdata)))

(defvar livesMean (average (map 'list
                                (lambda (it) (third it))
                                workdata)))

(defun square (x)
  (expt x 2))

; scoreNumber += (X[i] - x_mean) * (Y[i] - y_mean)
(defvar scoreNumber (apply '+
                       (map 'list (lambda (it)
                                    (* (- (first it) scoremean ) (- (third it) livesMean))
                                  ) workdata)))

; divisor += (X[i] - x_mean)^2
(defvar sumOfSquaresForLives (apply '+
                         (map 'list (lambda (it)
                                      (square (- (third it) livesMean))
                                    ) workdata)))

(defvar b1 (/ scoreNumber sumOfSquaresForLives))

(defvar b0 scoremean)

(defun getScoreByLives (count)
  (+ b0 (* b1 count)))

; Середньоквадратична помилка очок - Σsqrt((predicted - actual)^2/n)
(defvar scoreRmse (sqrt (/ (apply '+ (map 'list (lambda (it)
                                           (square (- (first it) (getScoreByLives (third it))))
                                         ) workdata))
                    (length workdata))))

(print (format NIL " Score RMSE = ~F" scoreRmse))

(defvar timeNumber (apply '+
                       (map 'list (lambda (it)
                                    (* (- (second it) timeMean) (- (third it) livesMean))
                                  ) workdata)))

(defvar timeB1 (/ timeNumber sumOfSquaresForLives))

(defvar timeB0 (- timeMean (* timeB1 livesMean)))

(defun getTimeByLives (count)
  (+ timeB0 (* timeB1 count)))

; Середньоквадратична помилка часу - Σsqrt((predicted - actual)^2/n)
(defvar timeRmse (sqrt (/ (apply '+ (map 'list (lambda (it)
                                           (square (- (second it) (getTimeByLives (third it))))
                                         ) workdata))
                    (length workdata))))

(print (format NIL "TimeRMSE = ~F" timeRmse))

(defvar i 0)

(defun round (x)
  (fix ((if (minusp x) - +) x 0.5)))

(defvar newCsvFile (map 'list (lambda(it) (list ( if (> maxScore (second it)) "Lose" "Win"  ) (if (> maxScore (second it)) (round (second it)) 100) (third it) (first it))) (iter (for i from 1 to 5)
    (collect (list i  (getScoreByLives i) (getTimeByLives i))))))

(push (list "Status game" "Score" "Time" "Lives") newCsvFile)
(print newCsvFile)
(terpri)

(defun export-csv (row-data file)
  (with-open-file (stream file :direction :output)
    (fare-csv:write-csv-lines row-data stream)))

(export-csv newCsvFile #P"C:/Users/Кристина/PycharmProjects/pacman/predict_results.csv")
