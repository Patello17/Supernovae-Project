# Dataset(s) 27863, 28374
data = "combined_src.pi"
bkg_data = "combined_bkg.pi"
arf = "combined_src.arf"
bkg_arf = "2combined_bkg.arf"
rmf = "combined_src.rmf"
bkg_rmf = "2combined_bkg.rmf"

# Load and Group Data
load_pha(data)
notice(0.3,8)
subtract()
group_counts(15)

# Calculate Counts and Count Rate
data_sum = calc_data_sum()
print("Data Counts =", data_sum)
data_cnt_rate = calc_data_sum()/get_exposure()
print("Data Counts Rate =", data_cnt_rate)

set_xsxset("APECROOT", "/home/prayag/Software/ciao-4.17/spectral/modelData/apec_v3.0.9") # Use correct APECROOT
set_source(xstbabs.abs1*xsvapec.v1) # Fit APEC Model + Gaussian
# g1.Sigma=0.2
set_par("abs1.nH", min=0.0767)
v1.kT = 21
freeze(v1.kT) # freeze temperature like Chandra 2024 does
set_xsabund("wilm")
print("Configured.")

print("Fitting...")
fit()
fres = get_fit_results()
print(fres)
print("Fitted.")

print("Getting Confidence...")
conf()
confidence = get_conf_results()
print("Got Confidence.")

# Format Plot
print("Formatting Plot(s)...")
# plot("bkg")
set_ylog()
plot_fit(color="royalblue")
# plot_bkg_fit(overplot=True)
plt.xlim(0.3, 8)
plt.ylim(0, 0.015)

fig = plt.gcf()
ax1 = fig.axes[0]
ax2 = fig.axes[0]

plt.sca(ax1)
plt.ylabel("Counts s$^{-1}$ keV$^{-1}$", fontsize=14)
plt.yticks(fontsize=11)
ax1.lines[0].set_linewidth(4)
ax1.lines[2].set_color("sandybrown")
ax1.lines[2].set_linewidth(3)
plt.title("Swift Data Plot (Aug. 11, 2023 - Aug. 12, 2023)")
# plt.setp(ax1.spines.values(), linewidth=3)

plt.sca(ax2)
plt.ylabel("Counts s$^{-1}$ keV$^{-1}$", fontsize=14)
plt.yticks(fontsize=12)
plt.xticks(fontsize=12)
plt.xlabel("Energy (keV)", fontsize=14)
plt.setp(ax2.lines, linewidth=4)
# ax2.lines[0].set_linewidth(2)
plt.setp(ax2.spines.values(), linewidth=2)
print("Plot Formatted.")

# Get Flux
print("Calculating Flux...")
s1 = sample_flux(v1, 0.3, 8, num=1000) # Calculate Uncertainty for Flux
print("Calculated Flux.")

# Save Plot
print("Saving Plot...")
plt.savefig("2023ixf_plot.pdf")
print("Plot Saved.")

# Save Data
print("Saving Data...")
save_all("results.log", clobber=True) # Saves everything except the flux
absorbed_fluxes = s1[0]
unabsorbed_fluxes = s1[1]

def format_flux_stats(flux_array):
    return f"{flux_array[0]} +{flux_array[1] - flux_array[0]}, {flux_array[0] - flux_array[2]}"

absorbed_str = format_flux_stats(absorbed_fluxes)
unabsorbed_str = format_flux_stats(unabsorbed_fluxes)

# Save flux to file
with open("results.log", "a") as f: # "a" appends the flux
        f.write("\n######### Calculated Fluxes\n\n")
        f.write(f"Absorbed Flux: {absorbed_str}\n")
        f.write(f"Unabsorbed Flux: {unabsorbed_str}\n")
# Save confidence
        f.write("\n######### Calculated Confidences\n\n")
        f.write(f"{confidence}\n")
# Save counts and count rate
        f.write("\n######## Counts and Count Rate\n\n")
        f.write(f"Counts: {data_sum}\n")
        f.write(f"Count Rate: {data_cnt_rate}")

print("Data Saved.")

