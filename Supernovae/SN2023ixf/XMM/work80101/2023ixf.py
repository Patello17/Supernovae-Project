# Dataset(s) 0921180101
data_mos1 = "mos1spec_grp.fits"
bkg_data_mos1 = "mos1bgspec.fits"
arf_mos1 = "mos1.arf"
bkg_arf_mos1 = "mos1.arf"
rmf_mos1 = "mos1.rmf"
bkg_rmf_mos1 = "mos1.rmf"

data_mos2 = "mos2spec_grp.fits"
bkg_data_mos2 = "mos2bgspec.fits"
arf_mos2 = "mos2.arf"
bkg_arf_mos2 = "mos2.arf"
rmf_mos2 = "mos2.rmf"
bkg_rmf_mos2 = "mos2.rmf"

data_pn = "pnspec_grp.fits"
bkg_data_pn = "pnbgspec.fits"
arf_pn = "pn.arf"
bkg_arf_pn = "pn.arf"
rmf_pn = "pn.rmf"
bkg_rmf_pn = "pn.rmf"

# Load and Group Data
load_pha(1, data_mos1)
load_arf(1, arf_mos1)
load_rmf(1, rmf_mos1)
load_pha(2, data_mos2)
load_arf(2, arf_mos2)
load_rmf(2, rmf_mos2)
load_pha(3, data_pn)
load_arf(3, arf_pn)
load_rmf(3, rmf_pn)
notice(0.3, 8)
subtract(1)
subtract(2)
subtract(3)
group_counts(1, 15)


# Calculate Counts and Count Rate
data_sum_1 = calc_data_sum(id=1)
print("Data Counts (MOS1) =", data_sum_1)
data_cnt_rate_1 = calc_data_sum(id=1)/get_exposure(id=1)
print("Data Counts Rate (MOS1) =", data_cnt_rate_1)

data_sum_2 = calc_data_sum(id=2)
print("Data Counts (MOS2) =", data_sum_2)
data_cnt_rate_2 = calc_data_sum(id=2)/get_exposure(id=2)
print("Data Counts Rate (MOS2) =", data_cnt_rate_2)

data_sum_3 = calc_data_sum(id=3)
print("Data Counts (PN) =", data_sum_3)
data_cnt_rate_3 = calc_data_sum(id=3)/get_exposure(id=3)
print("Data Counts Rate (PN) =", data_cnt_rate_3)

set_xsxset("APECROOT", "/home/prayag/Software/ciao-4.17/spectral/modelData/apec_v3.0.9") # Use correct APECROOT
set_source(1, xstbabs.abs1*xsvapec.v1) # Fit APEC Model
set_source(2, xstbabs.abs1*xsvapec.v1) # Fit APEC Model
set_source(3, xstbabs.abs1*xsvapec.v1) # Fit APEC Model
set_par("abs1.nH", min=0.0767)
# thaw(v1.Fe)
set_xsabund("wilm")
print("Configured.")

print("Fitting...")
fit(1)
fit(2)
fit(3)
fres = get_fit_results()
print(fres)
print("Fitted.")

print("Getting Confidence...")
conf(1)
confidence_1 = get_conf_results()
conf(2)
confidence_2 = get_conf_results()
conf(3)
confidence_3 = get_conf_results()
print("Got Confidence.")

# Format Plot
print("Formatting Plot(s)...")
# plot("bkg")
set_ylog()
# plot("fit", 1, "fit", 2)
plot("fit", 1, "fit", 2, "fit", 3, color="blue")
# plot_bkg_fit(overplot=True)
# plt.xlim(0.3, 8)
# # plt.ylim(0, 0.015)

# fig = plt.gcf()
# ax1 = fig.axes[0]
# ax2 = fig.axes[0]

# plt.sca(ax1)
# plt.ylabel("Counts s$^{-1}$ keV$^{-1}$", fontsize=14)
# plt.yticks(fontsize=11)
# ax1.lines[0].set_linewidth(4)
# ax1.lines[2].set_color("sandybrown")
# ax1.lines[2].set_linewidth(3)
# plt.title("XMM Data Plot (June 18, 2023)")
# # plt.setp(ax1.spines.values(), linewidth=3)

# plt.sca(ax2)
# plt.ylabel("Counts s$^{-1}$ keV$^{-1}$", fontsize=14)
# plt.yticks(fontsize=12)
# plt.xticks(fontsize=12)
# plt.xlabel("Energy (keV)", fontsize=14)
# plt.setp(ax2.lines, linewidth=4)
# # ax2.lines[0].set_linewidth(2)
# plt.setp(ax2.spines.values(), linewidth=2)
# print("Plot Formatted.")

# Get Flux
print("Calculating Flux...")
s1 = sample_flux(v1, 0.3, 8, 1, num=1000) # Calculate Uncertainty for Flux
s2 = sample_flux(v1, 0.3, 8, 2, num=1000) # Calculate Uncertainty for Flux
s3 = sample_flux(v1, 0.3, 8, 3, num=1000) # Calculate Uncertainty for Flux
print("Calculated Flux.")

# Save Plot
print("Saving Plot...")
plt.savefig("2023ixf_plot.pdf")
print("Plot Saved.")

# Save Data
print("Saving Data...")
save_all("results.log", clobber=True) # Saves everything except the flux
absorbed_fluxes_mos1 = s1[0]
unabsorbed_fluxes_mos1 = s1[1]
absorbed_fluxes_mos2 = s2[0]
unabsorbed_fluxes_mos2 = s2[1]
absorbed_fluxes_pn = s3[0]
unabsorbed_fluxes_pn = s3[1]

def format_flux_stats(flux_array):
    return f"{flux_array[0]} +{flux_array[1] - flux_array[0]}, {flux_array[0] - flux_array[2]}"

absorbed_str_mos1 = format_flux_stats(absorbed_fluxes_mos1)
unabsorbed_str_mos1 = format_flux_stats(unabsorbed_fluxes_mos1)
absorbed_str_mos2 = format_flux_stats(absorbed_fluxes_mos2)
unabsorbed_str_mos2 = format_flux_stats(unabsorbed_fluxes_mos2)
absorbed_str_pn = format_flux_stats(absorbed_fluxes_pn)
unabsorbed_str_pn = format_flux_stats(unabsorbed_fluxes_pn)

# Save flux to file
with open("results.log", "a") as f: # "a" appends the flux
        f.write("\n######### Calculated Fluxes\n\n")
        f.write(f"Absorbed Flux (MOS1): {absorbed_str_mos1}\n")
        f.write(f"Unabsorbed Flux (MOS1): {unabsorbed_str_mos1}\n")
        f.write(f"Absorbed Flux (MOS2): {absorbed_str_mos2}\n")
        f.write(f"Unabsorbed Flux (MOS2): {unabsorbed_str_mos2}\n")
        f.write(f"Absorbed Flux (PN): {absorbed_str_pn}\n")
        f.write(f"Unabsorbed Flux (PN): {unabsorbed_str_pn}\n")
# Save confidence
        f.write("\n######### Calculated Confidences\n\n")
        f.write(f"MOS1: {confidence_1}\n")
        f.write(f"MOS2: {confidence_2}\n")
        f.write(f"PN: {confidence_3}\n")
# Save counts and count rate
        f.write("\n######## Counts and Count Rate\n\n")
        f.write(f"Counts (MOS1): {data_sum_1}\n")
        f.write(f"Count Rate (MOS1): {data_cnt_rate_1}\n")
        f.write(f"Counts (MOS2): {data_sum_2}\n")
        f.write(f"Count Rate (MOS2): {data_cnt_rate_2}\n")
        f.write(f"Counts (PN): {data_sum_3}\n")
        f.write(f"Count Rate (PN): {data_cnt_rate_3}\n")

print("Data Saved.")