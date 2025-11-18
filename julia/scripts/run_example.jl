using Pkg
Pkg.activate("..")
Pkg.instantiate()

using FSSLib

x = range(-5, 5, length=201)
y = dummy_catenary(x, H=10.0, w=2.0)
k = example_mooring_stiffness(100.0, 1e6)

println("Catenary y-range: ", minimum(y), " to ", maximum(y))
println("Example mooring stiffness: ", k)
