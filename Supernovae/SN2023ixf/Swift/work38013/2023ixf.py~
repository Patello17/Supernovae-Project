data = "combined_src.pi"

# Load and Group Data
load_data("combined_src.pi")
notice(0.3,8)
subtract()
group_counts(15)

set_xsxset("APECROOT", "/home/prayag/Software/ciao-4.17/spectral/modelData/apec_v3.0.9") # Use correct APECROOT
set_source(xstbabs.abs1*xsvapec.v1) # Fit APEC Model
# set_source(xstbabs.abs1*xsvmekal.v1)
# g1.Sigma=0.2 # (No Gaussian Necessary)
set_xsabund("wilm")
# thaw(v1.Si)

fit()
fres = get_fit_results()

# conf()
# set_ylog()


plot_fit_delchi(color="blue")
plt.xlim(0.3,8)

# Format Plot
fig = plt.gcf()
ax1, ax2 = fig.axes

plt.sca(ax1)
plt.ylabel("Counts s$^{-1}$ keV$^{-1}$", fontsize=14)
plt.yticks(fontsize=11)
#ax1.lines[0].set_linewidth(4)
ax1.lines[2].set_color("orange")
ax1.lines[2].set_linewidth(3)
plt.title("2023ixf APEC Model Fit (Sources: Chandra 27863 & 28374)")
plt.setp(ax1.spines.values(), linewidth=3)

plt.sca(ax2)
plt.ylabel('Sigma', fontsize=14)
plt.yticks(fontsize=12)
plt.xticks(fontsize=12)
plt.xlabel('Energy (keV)', fontsize=14)
#plt.setp(ax2.lines, linewidth=4)

ax2.lines[0].set_linewidth(2)

plt.setp(ax2.spines.values(), linewidth=2)

# s1=sample_flux(v1+g1,0.3,8,num=1000) # Calculate uncertainty for flux
plt.savefig("2023ixf_plot.pdf")
