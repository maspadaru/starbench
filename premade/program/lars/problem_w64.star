warn(X1, X2) := [$, 64] [D] p(X1, X2)
error(X1, X2) := [$, 64] [B] q(X1, X2)
prob(X1,X2) := error(X1, X2) && warn(X1, X2) 
