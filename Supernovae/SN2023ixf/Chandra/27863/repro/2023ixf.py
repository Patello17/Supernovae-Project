load_data("2023ixf_grp.pi")
notice(0.3,8)
plot_data()
subtract()

set_xsxset("APECROOT", "/home/prayag/Software/ciao-4.17/spectral/modelData/apec_v3.0.9")

set_source(xstbabs.abs1*(xsvapec.v1+xsgaussian.g1))
g1=Sigma=0.2
set_xsabund("wilm")
thaw(v1.Si)
fit()
conf()
plot_fit_delchi()
s1=sample_flux(v1+g1,0.3,8,num=1000) # Calculate uncertainty for flux
plt.savefig("2023ixf_plot.pdf")
