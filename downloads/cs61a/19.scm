; Begin example

; (if (define x 10) (> x 10) 'hello 'world)
; (if (begin (define x 10) (> x 10)) 'hello 'world)

; Let example
; (let ((x 10) (y 5)) (+ x y))
; x
; y
; (begin (define x 10) (define y 5) (+ x y))
; x
; y

; List demos

(define s (cons 1 (cons 2 (cons 3 (cons 4 nil)))))
s
(car s)
(car (cdr s))
(car (cdr (cdr s)))
(car (cdr (cdr (cdr s))))

s
(cdr s)
(cdr (cdr s))
(cdr (cdr (cdr s)))
(car (cdr (cdr (cdr s))))

(cons 5 s)
(cons 6 (cons 5 s))
(cons (cons 6 (cons 5 nil)) s)
(car (car (cons (cons 6 (cons 5 nil)) s)))
(cons s (cons s nil))

(cons 1 (cons (cons 2 nil) (cons 3 nil)))
; ?
; (1 (2 3) 4)
; (cons 1 (cons (cons 2 (cons 3 nil)) (cons 4 nil)))

(define t (cons 1 (cons (cons 2 (cons 3 nil)) (cons 4 nil))))
t
; write an expression using `t` that extracts the `3`
(car (cdr (car (cdr t))))

; List Construction

(list 1 2)
(list 1 2 3 4)
(cdr (list 1 2 3 4))
(cons 0 (cdr (list 1 2 3 4)))

(list s)
(list 3 s)
(cons 3 s)
(list s s)
(cons s s)

(define t (list 2 3 4))
(define u (list 5 6 7))
(list t u)
(cons t u)
(append t u)

; https://code.cs61a.org/
(define u (list 2 3 4))
u
(draw u)
(list u u)
(draw (list u u))
(list (list 2 3 4) (list 6 7 8))
(draw (list (list 2 3 4) (list 6 7 8)))

; Other Built-in List Procedures

(list? s)
(list? nil)
(list? 4)
(null? nil)
(null? s)

; Recursive List Construction

;;; Return a list of two lists; the first n elements of s and the rest
;;; scm> (split (list 3 4 5 6 7 8) 3)
;;; ((3 4 5) (6 7 8))
(define (split s n)
  ; The first n elements of s
  (define (prefix s n)
    (if (zero? n) ___ (_____ ________ (prefix _______ (- n 1)))))
  ; The elements after the first n
  (define (suffix s n)
    (if (zero? n) ___ ________________________))
  (_____ (prefix s n) (suffix s n)))


;;; Return a list of two lists; the first n elements of s and the rest
;;; scm> (split (list 3 4 5 6 7 8) 3)
;;; ((3 4 5) (6 7 8))
(define (split s n)
  ; The first n elements of s
  (define (prefix s n)
    (if (zero? n) nil (cons (car s) (prefix (cdr s) (- n 1)))))
  ; The elements after the first n
  (define (suffix s n)
    (if (zero? n) s (suffix (cdr s) (- n 1))))
  (list (prefix s n) (suffix s n)))


; v2
;;; Return a list of two lists; the first n elements of s and the rest
;;; scm> (split (list 3 4 5 6 7 8) 3)
;;; ((3 4 5) (6 7 8))
(define (split s n)
  (if (= n 0) 
      _____________
      (let ((split-rest (split (cdr s) (- n 1)))) 
	      (_____ _______________________________
	             (cdr split-rest)))))

(define (split s n)
  (if (= n 0) 
      (list nil s) 
      (let ((split-rest (split (cdr s) (- n 1)))) 
	(cons (cons (car s) (car split-rest)) 
	      (cdr split-rest)))))

; Quotation demos

(define s (list 2 3 4))
(define t (list 5 6 7))
s
t
's
't
(quote s)
(list s t)
(list 's 't)
's
'(2 3 4)
(car '(2 3 4))
(cdr '(2 3 4))

; List Processing

(1 2 3 4)                                 ; count
((and a 1) (and a 2) (and a 3) (and a 4)) ; beats
(and a 1 and a 2 and a 3 and a 4)         ; rhythm

(define count (list 1 2 3 4))
(define beats (map ______________________________ count))
(define rhythm (______ _______ beats))

(define count (list 1 2 3 4))
(define beats (map (lambda (x) (list 'and 'a x)) count))
(define rhythm (apply append beats))

; Extra Quotation Demos

'(1 2 3)
(quote (1 2 3))
'(1 (2 3) 4)
(car (cdr (car (cdr '(1 (2 3) 4)))))
(car (cdr (car (cdr '(a (b c) d)))))
'(+ 1 2)
(car (quote (+ 1 2)))
(car '(+ 1 2))
(cons '+ (list 1 2))
