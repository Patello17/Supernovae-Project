load_pha("pnspec_grp.fits")
notice(0.3, 8)
subtract()
group_counts(25)

data_sum = calc_data_sum()
print("Data Counts =", data_sum)
data_cnt_rate = calc_data_sum(id=1)/get_exposure()
print("Data Counts Rate =", data_cnt_rate)

set_xsxset("APECROOT", "/home/prayag/Software/ciao-4.17/spectral/modelData/apec_v3.0.9") # Use correct APECROOT
set_source(xstbabs.abs1*(xsvapec.v1+xsgaussian.g1)+xstbabs.abs2*xspowerlaw.p1) # Fit APEC Model
set_par("g1.Sigma", val=0.2, frozen=True)
set_par("v1.Redshift", val=0.0008, frozen=True)
set_par("abs2.nH", val=0.44, frozen=True) # from Nayana et al. 2025
set_par("p1.PhoIndex", val=5.5, frozen=True) # from Nayana et al. 2025
# set_par("abs2.gamma", val=5.5, frozen=True)
# set_par("v2.Redshift", val=0.0008, frozen=True)
set_par("abs1.nH", min=0.0767)
set_xsabund("wilm")

fit()

set_ylog()
plot_fit_delchi()

sample_flux(v1+g1, 0.3, 8, num=1000)
