# Dataset(s) 90902520006
data_A = "../productsA/nu90902520006A01_sr.pha"
bkg_data_A = "../productsA/nu90902520006A01_bk.pha"
arf_A = "../productsA/nu90902520006A01_sr.arf"
bkg_arf_A = "../productsA/nu90902520006A01_sr.arf"
rmf_A = "../productsA/nu90902520006A01_sr.rmf"
bkg_rmf_A = "../productsA/nu90902520006A01_sr.rmf"

data_B = "../productsB/nu90902520006B01_sr.pha"
bkg_data_B = "../productsB/nu90902520006B01_bk.pha"
arf_B = "../productsB/nu90902520006B01_sr.arf"
bkg_arf_B = "../productsB/nu90902520006B01_sr.arf"
rmf_B = "../productsB/nu90902520006B01_sr.rmf"
bkg_rmf_B = "../productsB/nu90902520006B01_sr.rmf"

# Load and Group Data
# Load and Group Data
load_pha(1, data_A)
load_pha(2, data_B)
load_arf(1, arf_A)
load_arf(2, arf_B)
load_rmf(1, rmf_A)
load_rmf(2, rmf_B)
notice(0.3,8)
subtract(1)
subtract(2)
group_counts(1, 15)
group_counts(2, 15)

# Calculate Counts and Count Rate
data_sum = calc_data_sum()
print("Data Counts =", data_sum)
data_cnt_rate = calc_data_sum()/get_exposure()
print("Data Counts Rate =", data_cnt_rate)

set_xsxset("APECROOT", "/home/prayag/Software/ciao-4.17/spectral/modelData/apec_v3.0.9") # Use correct APECROOT
set_source(1, xstbabs.abs1*xsvapec.v1) # Fit APEC Model
set_source(2, abs1*v1) # Fit APEC Model
# g1.Sigma=0.2
set_par("abs1.nH", min=0.0767)
# thaw(v1.Fe)
set_xsabund("wilm")
print("Configured.")

print("Fitting...")
fit(1, 2)
fres = get_fit_results()
print(fres)
print("Fitted.")

print("Getting Confidence...")
conf(1, 2)
confidence = get_conf_results()
print("Got Confidence.")

# Format Plot
print("Formatting Plot(s)...")
# plot("bkg")
set_ylog()
# plot("fit", 1, "fit", 2)
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