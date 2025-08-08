load_pha("mos1spec_grp.fits")
notice(0.3, 8)
subtract()
group_counts(25)

# Calculate Counts and Count Rate
data_sum = calc_data_sum()
print("Data Counts =", data_sum)
data_cnt_rate = calc_data_sum(id=1)/get_exposure()
print("Data Counts Rate =", data_cnt_rate)

set_xsxset("APECROOT", "/home/prayag/Software/ciao-4.17/spectral/modelData/apec_v3.0.9") # Use correct APECROOT
set_source(xstbabs.abs1*(xsvapec.v1)) # Fit APEC Model
set_par("v1.Redshift", val=0.0008, frozen=True)
set_par("abs1.nH", min=0.0767)
set_xsabund("wilm")

fit()

set_ylog()
plot_fit_delchi()

sample_flux(v1, 0.3, 8, num=1000)
