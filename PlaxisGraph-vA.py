# import libraries
import streamlit as st
import pandas as pd
import os
import glob
import seaborn as sns
import matplotlib.pyplot as plt

st.title('PLAXIS2D Analysis Output')

# import csv into a dataframe
path = os.path.join(os.path.expanduser('~'),'Downloads')
all_files = glob.glob(os.path.join(path, "*.txt"))

data = []

for f in all_files:
    df_eachfile = (pd.read_csv(f, delimiter ="\t", encoding = "ISO-8859-1",skiprows=[3]))
    file_name = os.path.basename(f)
    df_eachfile['filename'] = os.path.splitext(file_name)[0]
    data.append(df_eachfile)
    
df_concat = pd.concat(data, ignore_index=True)

# change ux uy from m to mm
df_concat["u_x"] = 1000 * df_concat["u_x"]
df_concat["u_y"] = 1000 * df_concat["u_y"]

# add stage number as sort
df_concat['sort'] = df_concat['filename'].str.extract(r'(\d+)-', expand=False).astype(int)

# extract stage name from filename
df_concat['Stage'] = df_concat['filename'].str.split('[').str[0]
df_concat['Stage'] = df_concat['Stage'].str.split('-').str[1]

# convert value to abs
df_concat['Lateral Displacement (mm)'] = df_concat['u_x'].abs()
df_concat['Vertical Displacement (mm)'] = df_concat['u_y'].abs()
df_concat['Bending Moment (kNm/m)'] = df_concat['M'].abs()
df_concat['Shear Force (kN/m)'] = df_concat['Q'].abs()
df_concat['Axial Force (kN/m)'] = df_concat['N'].abs()

# select columns
df1 = df_concat.loc[:, ['Stage',
                        'Lateral Displacement (mm)',
                        'Vertical Displacement (mm)',
                        'Bending Moment (kNm/m)',
                        'Shear Force (kN/m)',
                        'Axial Force (kN/m)',
                        'sort']].copy() 

# create table
st.markdown('Summary Table')
df_stage = df1.groupby("sort")
table_max = df_stage.max()
table_max.style.set_properties(**{'text-align': 'center'})
table_max.style.format(precision=0, na_rep='MISSING')
st.table(table_max)


# create colour
sns.set_palette("colorblind")

# create figures
f = plt.figure(figsize=(10, 6))
gs = f.add_gridspec(1, 4)

with sns.axes_style("darkgrid"):
    ax0 = f.add_subplot(gs[0, 0])
    sns.lineplot(x="u_x", y="Y", hue="Stage", style="Stage", sort=False, legend=False, data=df_concat)

    ax1 = f.add_subplot(gs[0, 1])
    sns.lineplot(x="M", y="Y", hue="Stage", style="Stage", sort=False, legend=False, data=df_concat)

    ax2 = f.add_subplot(gs[0, 2])
    sns.lineplot(x="Q", y="Y", hue="Stage", style="Stage", sort=False, legend=False, data=df_concat)   

    ax3 = f.add_subplot(gs[0, 3])
    sns.lineplot(x="N", y="Y", hue="Stage", style="Stage", sort=False, legend=False, data=df_concat)

# set axis
ax0.set_ylabel('Elevation (m AHD)') 
ax1.yaxis.label.set_visible(False)
ax2.yaxis.label.set_visible(False)
ax3.yaxis.label.set_visible(False)

ax1.set_yticklabels([])
ax2.set_yticklabels([])
ax3.set_yticklabels([])

ax0.set_xlabel('Displacement (mm)') 
ax1.set_xlabel('Bending Moment (kNm/m)') 
ax2.set_xlabel('Shear Force (kN/m)') 
ax3.set_xlabel('Axial Force (kN/m)') 

ax0.xaxis.set_ticks_position("top")
ax1.xaxis.set_ticks_position("top")
ax2.xaxis.set_ticks_position("top")
ax3.xaxis.set_ticks_position("top")

ax0.xaxis.set_ticks_position('none') 
ax1.xaxis.set_ticks_position('none') 
ax2.xaxis.set_ticks_position('none') 
ax3.xaxis.set_ticks_position('none') 

ax0.xaxis.set_label_position("top")
ax1.xaxis.set_label_position("top")
ax2.xaxis.set_label_position("top")
ax3.xaxis.set_label_position("top")

# create the legend
line_labels = df1['Stage'].unique()

f.legend(labels=line_labels,   # The labels for each line
           bbox_to_anchor=(.9,0.5),
           loc="center left",   # Position of legend
           borderaxespad=0.1,    # Small spacing around legend box
           title="Stage"  # Title for the legend
           )

# adjust the scaling factor to fit your legend text completely outside the plot
plt.subplots_adjust(right=0.9) # smaller value results in more space being made for the legend
#export figure
plt.savefig(os.path.join(path, "Plaxis graph.png"), bbox_inches='tight',dpi=600)

# create plot
st.markdown('Summary Graph')
st.pyplot(f)

st.write('Summary completed')