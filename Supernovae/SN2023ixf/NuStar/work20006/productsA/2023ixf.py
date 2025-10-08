# Dataset(s) 90902520006
data = "nu90902520006A01_sr.pha"
bkg_data = "nu90902520006A01_bk.pha"
arf = "nu90902520006A01_sr.arf"
bkg_arf = "nu90902520006A01_sr.arf"
rmf = "nu90902520006A01_sr.rmf"
bkg_rmf = "nu90902520006A01_sr.rmf"

# Load and Group Data
load_pha(data)
load_arf(arf)
load_rmf(rmf)
notice(3, 78.4)
subtract()
group_counts(15)


# Calculate Counts and Count Rate
data_sum = calc_data_sum()
print("Data Counts =", data_sum)
data_cnt_rate = calc_data_sum()/get_exposure()
print("Data Counts Rate =", data_cnt_rate)

set_xsxset("APECROOT", "/home/prayag/Software/ciao-4.17/spectral/modelData/apec_v3.0.9") # Use correct APECROOT
set_source(1, xstbabs.abs1*(xsvapec.v1+xsgaussian.g1)) # Fit APEC Model
guess()
# set_par("g1.Sigma", val=0.2)
set_par("g1.LineE", val=6.5, frozen=False)
set_par("abs1.nH", min=0.0767)
set_par("v1.Redshift", val=0.0008, frozen=True)
# thaw(v1.Fe)
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
# plot("fit", 1, "fit", 2)
plot_fit(color="royalblue")
# plot_bkg_fit(overplot=True)
plt.xlim(3, 78.4)
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
plt.title("NuStar Data Plot (June 8, 2023)")
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
s1 = sample_flux(v1+g1, 3, 78.4, num=1000) # Calculate Uncertainty for Flux
s2 = sample_flux(g1, 3, 78.4, num=1000) # Calculate Uncertainty for Flux due to Gaussian
# print(s2)
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
absorbed_guassian_fluxes = s2[0]
unabsorbed_guassian_fluxes = s2[1]

def format_flux_stats(flux_array):
    return f"{flux_array[0]} +{flux_array[1] - flux_array[0]}, {flux_array[0] - flux_array[2]}"

absorbed_str = format_flux_stats(absorbed_fluxes)
unabsorbed_str = format_flux_stats(unabsorbed_fluxes)
absorbed_g_str = format_flux_stats(absorbed_guassian_fluxes)
unabsorbed_g_str = format_flux_stats(unabsorbed_guassian_fluxes)

# Save flux to file
with open("results.log", "a") as f: # "a" appends the flux
        f.write("\n######### Calculated Fluxes\n\n")
        f.write(f"Absorbed Flux: {absorbed_str}\n")
        f.write(f"Unabsorbed Flux: {unabsorbed_str}\n")
        f.write(f"Absorbed Flux (due to Guassian): {absorbed_g_str}\n")
        f.write(f"Unabsorbed Flux (due to Guassian): {unabsorbed_g_str}\n")
# Save confidence
        f.write("\n######### Calculated Confidences\n\n")
        f.write(f"{confidence}\n")
# Save counts and count rate
        f.write("\n######## Counts and Count Rate\n\n")
        f.write(f"Counts: {data_sum}\n")
        f.write(f"Count Rate: {data_cnt_rate}")

print("Data Saved.")