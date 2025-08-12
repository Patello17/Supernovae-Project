load_pha("mos2spec_grp.fits")
notice(0.3, 8)
subtract()
group_counts(25)

data_sum = calc_data_sum()
print("Data Counts =", data_sum)
data_cnt_rate = calc_data_sum(id=1)/get_exposure()
print("Data Counts Rate =", data_cnt_rate)

set_xsxset("APECROOT", "/home/prayag/Software/ciao-4.17/spectral/modelData/apec_v3.0.9") # Use correct APECROOT
set_source(xstbabs.abs1*(xsvapec.v1+xsgaussian.g1)) # Fit APEC Model
set_par("v1.Redshift", val=0.0008, frozen=True)
set_par("abs1.nH", min=0.0767)
set_par("g1.Sigma", val=0.2, frozen=True)
# set_par("abs2.nH", val=0.44, frozen=True) # from Nayana et al. 2025
# set_par("p1.PhoIndex", val=5.5, frozen=True) # from Nayana et al. 2025
# set_par("abs2.gamma", val=5.5, frozen=True)
# set_par("v2.Redshift", val=0.0008, frozen=True)
set_xsabund("wilm")

fit()

print("Getting Confidence...")
conf()
confidence = get_conf_results()
print("Got Confidence.")

set_ylog()
plot_fit_delchi()

s1 = sample_flux(v1+g1, 0.3, 8, num=1000)
s2 = sample_flux(g1, 0.3, 8, num=1000)
# s3 = sample_flux(p1, 0.3, 1.8, num=1000)

# Save Plot
print("Saving Plot...")
plt.savefig("2023ixf_pnplot.pdf")
print("Plot Saved.")

# Save Data
print("Saving Data...")
save_all("results_mos2.log", clobber=True) # Saves everything except the flux
absorbed_fluxes = s1[0]
unabsorbed_fluxes = s1[1]
absorbed_fluxes_gauss = s2[0]
unabsorbed_fluxes_gauss = s2[1]
# absorbed_fluxes_power = s3[0]
# unabsorbed_fluxes_power = s3[1]

def format_flux_stats(flux_array):
    return f"{flux_array[0]} +{flux_array[1] - flux_array[0]}, {flux_array[0] - flux_array[2]}"

absorbed_str = format_flux_stats(absorbed_fluxes)
unabsorbed_str = format_flux_stats(unabsorbed_fluxes)

# Save flux to file
with open("results_mos2.log", "a") as f: # "a" appends the flux
        f.write("\n######### Calculated Fluxes\n\n")
        f.write(f"Absorbed Flux (v1+g1): {absorbed_str}\n")
        f.write(f"Unabsorbed Flux (v1+g1): {unabsorbed_str}\n")
        f.write(f"Absorbed Flux (Gaussian): {absorbed_str}\n")
        f.write(f"Unabsorbed Flux (Gaussian): {unabsorbed_str}\n")
        # f.write(f"Absorbed Flux (Power Law): {absorbed_str}\n")
        # f.write(f"Unabsorbed Flux (Power Law): {unabsorbed_str}\n")
# Save confidence
        f.write("\n######### Calculated Confidences\n\n")
        f.write(f"{confidence}\n")
# Save counts and count rate
        f.write("\n######## Counts and Count Rate\n\n")
        f.write(f"Counts: {data_sum}\n")
        f.write(f"Count Rate: {data_cnt_rate}")

print("Data Saved.")