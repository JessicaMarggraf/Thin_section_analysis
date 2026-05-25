# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 10:37:16 2025

@author: jmarggra

See description in Supporting information in Marggraf et al. & on https://github.com/JessicaMarggraf/Thin_section_analysis

"""

# Import libraries
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import re
from pathlib import Path
from matplotlib.lines import Line2D

#%% Define paths and scaling
scaling_px_um = 1.84 # 5x magnification, defined by microscope resolution

# csv file with total area in px2 for each thin section, labelling for lithology and thin sections
data_ts = pd.read_csv(r'C:\Users\jmarggra\Documents\Analysis\Thin_sections\Analysis_thin_sections_area.csv') # 'Analysis_thin_sections_area.csv'

main_folder = r'C:\Users\jmarggra\Documents\Analysis\Thin_sections' # main folder with subfolders for each thin section
file_name = "path_areas.txt" # Output from path_areas script in photoshop
outpath_figures = r'C:\Users\jmarggra\Documents\Analysis\Thin_sections\Figures' # outpath folder for figures

#%% Load data
file_contents = {}
for subfolder in os.listdir(main_folder):
    subfolder_path = os.path.join(main_folder, subfolder)
    if os.path.isdir(subfolder_path):
        file_path = os.path.join(subfolder_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                # Store content using subfolder name as key
                file_contents[subfolder] = f.read()

# Prepare data
GB_top1_px = file_contents['GB_Top1_5x']
GB_top2_px = file_contents['GB_Top2_5x']
GB_top3_px = file_contents['GB_Top3_5x']
GB_top4_px = file_contents['GB_Top4_5x']
GB_top5_px = file_contents['GB_Top5_5x']
GB_top6_px = file_contents['GB_Top6_5x']
Lester_top1_px = file_contents['Lester_Top1_5x']
Lester_top2_px = file_contents['Lester_Top2_5x']
Lester_top3_px = file_contents['Lester_Top3_5x']
Lester_top4_px = file_contents['Lester_Top4_5x']

GB_top1_px = GB_top1_px.split("\\n")
GB_top2_px = GB_top2_px.split("\\n")
GB_top3_px = GB_top3_px.split("\\n")
GB_top4_px = GB_top4_px.split("\\n")
GB_top5_px = GB_top5_px.split("\\n")
GB_top6_px = GB_top6_px.split("\\n")
Lester_top1_px = Lester_top1_px.split("\\n")
Lester_top2_px = Lester_top2_px.split("\\n")
Lester_top3_px = Lester_top3_px.split("\\n")
Lester_top4_px = Lester_top4_px.split("\\n")

GB_top1_px = GB_top1_px[1:-1]
GB_top2_px = GB_top2_px[1:-1]
GB_top3_px = GB_top3_px[1:-1]
GB_top4_px = GB_top4_px[1:-1]
GB_top5_px = GB_top5_px[1:-1]
GB_top6_px = GB_top6_px[1:-1]
Lester_top1_px = Lester_top1_px[1:-1]
Lester_top2_px = Lester_top2_px[1:-1]
Lester_top3_px = Lester_top3_px[1:-1]
Lester_top4_px = Lester_top4_px[1:-1]
        
substring = ": "
GB_top1_px = [re.sub(f".*?{re.escape(substring)}", "", GB_top1_px[i], count=1)
           for i in range(len(GB_top1_px))]
GB_top2_px = [re.sub(f".*?{re.escape(substring)}", "", GB_top2_px[i], count=1)
           for i in range(len(GB_top2_px))]
GB_top3_px = [re.sub(f".*?{re.escape(substring)}", "", GB_top3_px[i], count=1)
           for i in range(len(GB_top3_px))]
GB_top4_px = [re.sub(f".*?{re.escape(substring)}", "", GB_top4_px[i], count=1)
           for i in range(len(GB_top4_px))]
GB_top5_px = [re.sub(f".*?{re.escape(substring)}", "", GB_top5_px[i], count=1)
           for i in range(len(GB_top5_px))]
GB_top6_px = [re.sub(f".*?{re.escape(substring)}", "", GB_top6_px[i], count=1)
           for i in range(len(GB_top6_px))]
Lester_top1_px = [re.sub(f".*?{re.escape(substring)}", "", Lester_top1_px[i], count=1)
           for i in range(len(Lester_top1_px))]
Lester_top2_px = [re.sub(f".*?{re.escape(substring)}", "", Lester_top2_px[i], count=1)
           for i in range(len(Lester_top2_px))]
Lester_top3_px = [re.sub(f".*?{re.escape(substring)}", "", Lester_top3_px[i], count=1)
           for i in range(len(Lester_top3_px))]
Lester_top4_px = [re.sub(f".*?{re.escape(substring)}", "", Lester_top4_px[i], count=1)
           for i in range(len(Lester_top4_px))]
GB_top1_px = [float(line[:-4]) for line in GB_top1_px]
GB_top2_px = [float(line[:-4]) for line in GB_top2_px]
GB_top3_px = [float(line[:-4]) for line in GB_top3_px]
GB_top4_px = [float(line[:-4]) for line in GB_top4_px]
GB_top5_px = [float(line[:-4]) for line in GB_top5_px]
GB_top6_px = [float(line[:-4]) for line in GB_top6_px]
Lester_top1_px = [float(line[:-4]) for line in Lester_top1_px]
Lester_top2_px = [float(line[:-4]) for line in Lester_top2_px]
Lester_top3_px = [float(line[:-4]) for line in Lester_top3_px]
Lester_top4_px = [float(line[:-4]) for line in Lester_top4_px]

# drop values that are empty or 0
GB_top1_px = [x for x in GB_top1_px if x != 0]
GB_top2_px = [x for x in GB_top2_px if x != 0]
GB_top3_px = [x for x in GB_top3_px if x != 0]
GB_top4_px = [x for x in GB_top4_px if x != 0]
GB_top5_px = [x for x in GB_top5_px if x != 0]
GB_top6_px = [x for x in GB_top6_px if x != 0]
Lester_top1_px = [x for x in Lester_top1_px if x != 0]
Lester_top2_px = [x for x in Lester_top2_px if x != 0]
Lester_top3_px = [x for x in Lester_top3_px if x != 0]
Lester_top4_px = [x for x in Lester_top4_px if x != 0]

# convert from px to m
GB_top1_um = [GB_top1_px[i]/scaling_px_um**2 for i in range(len(GB_top1_px))]
GB_top1_cm = [GB_top1_um[i]*1e-8 for i in range(len(GB_top1_um))]
GB_top2_um = [GB_top2_px[i]/scaling_px_um**2 for i in range(len(GB_top2_px))]
GB_top2_cm = [GB_top2_um[i]*1e-8 for i in range(len(GB_top2_um))]
GB_top3_um = [GB_top3_px[i]/scaling_px_um**2 for i in range(len(GB_top3_px))]
GB_top3_cm = [GB_top3_um[i]*1e-8 for i in range(len(GB_top3_um))]
GB_top4_um = [GB_top4_px[i]/scaling_px_um**2 for i in range(len(GB_top4_px))]
GB_top4_cm = [GB_top4_um[i]*1e-8 for i in range(len(GB_top4_um))]
GB_top5_um = [GB_top5_px[i]/scaling_px_um**2 for i in range(len(GB_top5_px))]
GB_top5_cm = [GB_top5_um[i]*1e-8 for i in range(len(GB_top5_um))]
GB_top6_um = [GB_top6_px[i]/scaling_px_um**2 for i in range(len(GB_top6_px))]
GB_top6_cm = [GB_top6_um[i]*1e-8 for i in range(len(GB_top6_um))]
Lester_top1_um = [Lester_top1_px[i]/scaling_px_um**2 for i in range(len(Lester_top1_px))]
Lester_top1_cm = [Lester_top1_um[i]*1e-8 for i in range(len(Lester_top1_um))]
Lester_top2_um = [Lester_top2_px[i]/scaling_px_um**2 for i in range(len(Lester_top2_px))]
Lester_top2_cm = [Lester_top2_um[i]*1e-8 for i in range(len(Lester_top2_um))]
Lester_top3_um = [Lester_top3_px[i]/scaling_px_um**2 for i in range(len(Lester_top3_px))]
Lester_top3_cm = [Lester_top3_um[i]*1e-8 for i in range(len(Lester_top3_um))]
Lester_top4_um = [Lester_top4_px[i]/scaling_px_um**2 for i in range(len(Lester_top4_px))]
Lester_top4_cm = [Lester_top4_um[i]*1e-8 for i in range(len(Lester_top4_um))]

#%% Calculate total area of amygdules, percentage, etc.

data_ts['Total_area_um2'] = data_ts['Total_area_px2']/scaling_px_um**2
data_ts['Total_area_amygdules_px2'] = [np.sum(GB_top1_px), np.sum(GB_top2_px), np.sum(GB_top3_px), np.sum(GB_top4_px), np.sum(GB_top5_px), np.sum(GB_top6_px), 
                                       np.sum(Lester_top1_px), np.sum(Lester_top2_px), np.sum(Lester_top3_px), np.sum(Lester_top4_px)]
data_ts['Total_area_amygdules_um2'] = [np.sum(GB_top1_um), np.sum(GB_top2_um), np.sum(GB_top3_um), np.sum(GB_top4_um), np.sum(GB_top5_um), np.sum(GB_top6_um),
                                       np.sum(Lester_top1_um), np.sum(Lester_top2_um), np.sum(Lester_top3_um), np.sum(Lester_top4_um)]
data_ts['Total_area_amygdules_cm2'] = data_ts['Total_area_amygdules_um2']*1e-8
data_ts['Perc_area_amygdules'] = np.round(data_ts['Total_area_amygdules_um2']/data_ts['Total_area_um2']*100,3)
data_ts['Std_area_amygdules_um2'] = [np.std(GB_top1_um), np.std(GB_top2_um), np.std(GB_top3_um), np.std(GB_top4_um), np.std(GB_top5_um), np.std(GB_top6_um),
                                     np.std(Lester_top1_um), np.std(Lester_top2_um), np.std(Lester_top3_um), np.std(Lester_top4_um)]
data_ts['Percentile90_area_amygdules_um2'] = [np.percentile(GB_top1_um, 90), np.percentile(GB_top2_um, 90), np.percentile(GB_top3_um, 90), np.percentile(GB_top4_um, 90),
                                              np.percentile(GB_top5_um, 90),  np.percentile(GB_top6_um, 90), np.percentile(Lester_top1_um, 90), np.percentile(Lester_top2_um, 90), 
                                              np.percentile(Lester_top3_um, 90), np.percentile(Lester_top4_um, 90)]

#%% Plot histograms  

# GB_top1
fig, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=200)
plt.hist(GB_top1_cm, bins = 50, color='skyblue', edgecolor='black')
    
ax.set_xlabel('Area (cm2)', fontsize=18, weight = 'bold')
ax.set_ylabel('Frequency', fontsize=18, weight = 'bold')
ax.tick_params(axis = 'both', which = 'major', labelsize = 14)
ax.set_xlim(0,) 
ax.set_ylim(0,) 

fig.tight_layout()
figname = 'GB_top1_area_hist_cm2'
fig.savefig(outpath_figures+ '\\' + figname + '.png', dpi=100, bbox_inches='tight')

# GB_top2
fig, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=200)
plt.hist(GB_top2_cm, bins = 50, color='skyblue', edgecolor='black')
    
ax.set_xlabel('Area (cm2)', fontsize=18, weight = 'bold')
ax.set_ylabel('Frequency', fontsize=18, weight = 'bold')
ax.tick_params(axis = 'both', which = 'major', labelsize = 14)
ax.set_xlim(0,) 
ax.set_ylim(0,) 

fig.tight_layout()
figname = 'GB_top2_area_hist_cm2'
fig.savefig(outpath_figures+ '\\' + figname + '.png', dpi=100, bbox_inches='tight')

# GB_top3
fig, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=200)
plt.hist(GB_top3_cm, bins = 50, color='skyblue', edgecolor='black')
    
ax.set_xlabel('Area (cm2)', fontsize=18, weight = 'bold')
ax.set_ylabel('Frequency', fontsize=18, weight = 'bold')
ax.tick_params(axis = 'both', which = 'major', labelsize = 14)
ax.set_xlim(0,) 
ax.set_ylim(0,) 

fig.tight_layout()
figname = 'GB_top3_area_hist_cm2'
fig.savefig(outpath_figures+ '\\' + figname + '.png', dpi=100, bbox_inches='tight')

# GB_top4
fig, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=200)
plt.hist(GB_top4_cm, bins = 50, color='skyblue', edgecolor='black')
    
ax.set_xlabel('Area (cm2)', fontsize=18, weight = 'bold')
ax.set_ylabel('Frequency', fontsize=18, weight = 'bold')
ax.tick_params(axis = 'both', which = 'major', labelsize = 14)
ax.set_xlim(0,) 
ax.set_ylim(0,) 

fig.tight_layout()
figname = 'GB_top4_area_hist_cm2'
fig.savefig(outpath_figures+ '\\' + figname + '.png', dpi=100, bbox_inches='tight')


# GB_top5
fig, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=200)
plt.hist(GB_top5_cm, bins = 50, color='skyblue', edgecolor='black')
    
ax.set_xlabel('Area (cm2)', fontsize=18, weight = 'bold')
ax.set_ylabel('Frequency', fontsize=18, weight = 'bold')
ax.tick_params(axis = 'both', which = 'major', labelsize = 14)
ax.set_xlim(0,) 
ax.set_ylim(0,) 

fig.tight_layout()
figname = 'GB_top5_area_hist_cm2'
fig.savefig(outpath_figures+ '\\' + figname + '.png', dpi=100, bbox_inches='tight')

# GB_top6
fig, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=200)
plt.hist(GB_top6_cm, bins = 50, color='skyblue', edgecolor='black')
    
ax.set_xlabel('Area (cm2)', fontsize=18, weight = 'bold')
ax.set_ylabel('Frequency', fontsize=18, weight = 'bold')
ax.tick_params(axis = 'both', which = 'major', labelsize = 14)
ax.set_xlim(0,) 
ax.set_ylim(0,) 

fig.tight_layout()
figname = 'GB_top6_area_hist_cm2'
fig.savefig(outpath_figures+ '\\' + figname + '.png', dpi=100, bbox_inches='tight')

# Lester_top1
fig, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=200)
plt.hist(Lester_top1_cm, bins = 50, color='skyblue', edgecolor='black')
    
ax.set_xlabel('Area (cm2)', fontsize=18, weight = 'bold')
ax.set_ylabel('Frequency', fontsize=18, weight = 'bold')
ax.tick_params(axis = 'both', which = 'major', labelsize = 14)
ax.set_xlim(0,) 
ax.set_ylim(0,) 

fig.tight_layout()
figname = 'Lester_top1_area_hist_cm2'
fig.savefig(outpath_figures+ '\\' + figname + '.png', dpi=100, bbox_inches='tight')

# Lester_top2
fig, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=200)
plt.hist(Lester_top2_cm, bins = 50, color='skyblue', edgecolor='black')
    
ax.set_xlabel('Area (cm2)', fontsize=18, weight = 'bold')
ax.set_ylabel('Frequency', fontsize=18, weight = 'bold')
ax.tick_params(axis = 'both', which = 'major', labelsize = 14)
ax.set_xlim(0,) 
ax.set_ylim(0,) 

fig.tight_layout()
figname = 'Lester_top2_area_hist_cm2'
fig.savefig(outpath_figures+ '\\' + figname + '.png', dpi=100, bbox_inches='tight')

# Lester_top3
fig, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=200)
plt.hist(Lester_top3_cm, bins = 50, color='skyblue', edgecolor='black')
    
ax.set_xlabel('Area (cm2)', fontsize=18, weight = 'bold')
ax.set_ylabel('Frequency', fontsize=18, weight = 'bold')
ax.tick_params(axis = 'both', which = 'major', labelsize = 14)
ax.set_xlim(0,) 
ax.set_ylim(0,) 

fig.tight_layout()
figname = 'Lester_top3_area_hist_cm2'
fig.savefig(outpath_figures+ '\\' + figname + '.png', dpi=100, bbox_inches='tight')

# Lester_top4
fig, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=200)
plt.hist(Lester_top4_cm, bins = 50, color='skyblue', edgecolor='black')
    
ax.set_xlabel('Area (cm2)', fontsize=18, weight = 'bold')
ax.set_ylabel('Frequency', fontsize=18, weight = 'bold')
ax.tick_params(axis = 'both', which = 'major', labelsize = 14)
ax.set_xlim(0,) 
ax.set_ylim(0,) 

fig.tight_layout()
figname = 'Lester_top4_area_hist_cm2'
fig.savefig(outpath_figures+ '\\' + figname + '.png', dpi=100, bbox_inches='tight')

#%% Calculate diameters, areas etc

GB_top_cm = [GB_top1_cm, GB_top2_cm, GB_top3_cm, GB_top4_cm, GB_top5_cm, GB_top6_cm, 
                  Lester_top1_cm, Lester_top2_cm, Lester_top3_cm, Lester_top4_cm]

GB_top_cm_list = [item for sublist in GB_top_cm for item in sublist]
GB_top_cm = pd.DataFrame(GB_top_cm).transpose()
GB_top_cm.columns = ['Mng1', 'Mng2', 'Mng3', 'Mng4', 'Mng5', 'Mng6','Mnb1', 'Mnb2', 'Mnb3', 'Mnb4']
colorss = ["#4169E1", "#3A5EC9", "#4D76ED", "#3759BF", "#4B6FD6", "#2E52C2", "#228B22", "#1B6F1B", "#2E9B2E", "#1D7A46" ]
colorss = ["royalblue", "royalblue", "royalblue", "royalblue", "royalblue", "royalblue", "forestgreen", "forestgreen", "forestgreen", "forestgreen" ]
GB_top_mean_cm = GB_top_cm.mean().tolist()
GB_top_std_cm = GB_top_cm.std().tolist()

# calculate diameter of each amygdule assuming spheres
GB_top_diameter_cm = np.sqrt(GB_top_cm)
GB_top_diameter_mean_cm = GB_top_diameter_cm.mean().tolist()
GB_top_diameter_std_cm = GB_top_diameter_cm.std().tolist()

data_ts['Area_amygdules_mean_cm2'] = GB_top_mean_cm
data_ts['Area_amygdules_std_cm2'] = GB_top_std_cm
data_ts['Diameter_amygdules_mean_cm'] = GB_top_diameter_mean_cm
data_ts['Diameter_amygdules_std_cm'] = GB_top_diameter_std_cm
data_ts['Number_amygdules'] = GB_top_diameter_cm.count().tolist()

#%% Boxplot ts top
fig, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=200)

# sns.boxplot(data=GB_top_cm, palette=colorss)
ax = sns.violinplot(data=GB_top_cm, palette=colorss, inner="quart", linewidth=1.5, cut=0)
sns.stripplot(data=GB_top_cm, color="white",size=3, alpha=0.4, jitter=True)

ax.text(0, 0.28, ('n=' + str(len(GB_top1_cm))), fontsize = 14, ha='center')
ax.text(1, 0.28, ('n=' + str(len(GB_top2_cm))), fontsize = 14, ha='center')
ax.text(2, 0.28, ('n=' + str(len(GB_top3_cm))), fontsize = 14, ha='center')
ax.text(3, 0.28, ('n=' + str(len(GB_top4_cm))), fontsize = 14, ha='center')
ax.text(4, 0.28, ('n=' + str(len(GB_top5_cm))), fontsize = 14, ha='center')
ax.text(5, 0.28, ('n=' + str(len(GB_top6_cm))), fontsize = 14, ha='center')
ax.text(6, 0.28, ('n=' + str(len(Lester_top1_cm))), fontsize = 14, ha='center')
ax.text(7, 0.28, ('n=' + str(len(Lester_top2_cm))), fontsize = 14, ha='center')
ax.text(8, 0.28, ('n=' + str(len(Lester_top3_cm))), fontsize = 14, ha='center')
ax.text(9, 0.28, ('n=' + str(len(Lester_top4_cm))), fontsize = 14, ha='center')
        
ax.set_ylabel(r'Area (cm$\mathregular{^2}$)', fontsize=18, weight = 'bold')
ax.tick_params(axis = 'both', which = 'major', labelsize = 14)
ax.set_ylim(0,0.3) 

fig.tight_layout()
figname = 'Top_area_um2'
fig.savefig(outpath_figures+ '\\' + figname + '.png', dpi=100, bbox_inches='tight')
fig.savefig(outpath_figures+ '\\' + figname + '.pdf', dpi=100, bbox_inches='tight')

#%% Percentage ts top
fig, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=200)

ax.bar(data_ts['Thin_section'], data_ts['Perc_area_amygdules'], color = 'cornflowerblue')
        
# ax.set_ylabel(r'\mathregular{Area of amygdules \n total area (%)}', fontsize=20, weight = 'bold')
ax.tick_params(axis = 'both', which = 'major', labelsize = 16)
ax.set_ylim(0,) 

fig.tight_layout()
figname = 'Top_perc'
fig.savefig(outpath_figures+ '\\' + figname + '.png', dpi=300, bbox_inches='tight')

#%% ##############################################################################

# ANALYSE DISTANCE BETWEEN AMYGDULES

#%% ##############################################################################
# Load data
root_dir = Path(r"C:\Users\jmarggra\Documents\Analysis\Thin_sections")
target_suffix = "nearest_neighbor.csv" 
files = [p.resolve() for p in root_dir.rglob(f"*{target_suffix}") if p.is_file()]
filenames = [p.stem for p in root_dir.rglob(f"*{target_suffix}") if p.is_file()]

dfs_nearest_neighbor = []
for p in files:
    df = pd.read_csv(p)
    df["source_file"] = p.as_posix()   # full path; use p.name if you only want the filename
    dfs_nearest_neighbor.append(df)
all_nn = pd.concat(dfs_nearest_neighbor, ignore_index=True)

#%% Calculate mean and median distance

data_ts['Mean_distance_amygdules'] = [dfs_nearest_neighbor[i]['min_dist_phys_mum'].mean() for i in range(len(dfs_nearest_neighbor))]
data_ts['Median_distance_amygdules'] = [dfs_nearest_neighbor[i]['min_dist_phys_mum'].median() for i in range(len(dfs_nearest_neighbor))]
data_ts['Distance_amygdules_std'] = [dfs_nearest_neighbor[i]['min_dist_phys_mum'].std() for i in range(len(dfs_nearest_neighbor))]
for df in dfs_nearest_neighbor:
    df['min_dist_phys_cm'] = df['min_dist_phys_mum'] / 10000
data_ts['Mean_distance_amygdules_cm'] = [dfs_nearest_neighbor[i]['min_dist_phys_cm'].mean() for i in range(len(dfs_nearest_neighbor))]
data_ts['Median_distance_amygdules_cm'] = [dfs_nearest_neighbor[i]['min_dist_phys_cm'].median() for i in range(len(dfs_nearest_neighbor))]
data_ts['Distance_amygdules_cm_std'] = [dfs_nearest_neighbor[i]['min_dist_phys_cm'].std() for i in range(len(dfs_nearest_neighbor))]

#%% Plot histogram per thin section

for i in range(len(filenames)):
    fig, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=200)
    
    plt.hist(dfs_nearest_neighbor[i]['min_dist_phys_mum'], bins = 50, color='skyblue', edgecolor='black')
    ax.axvline(data_ts['Mean_distance_amygdules'][i], 0, 5, ls = '--', color = 'black', lw = 2, label = 'Mean')
    ax.axvline(data_ts['Median_distance_amygdules'][i], 0, 5, ls = ':', color = 'red', lw = 2, label = 'Median')
     
    ax.legend(loc = 'upper right', fontsize = 14)
    ax.set_xlabel(r'Distance ($\mathregular{\mu}$m)', fontsize=18, weight = 'bold')
    ax.set_ylabel('Frequency', fontsize=18, weight = 'bold')
    ax.tick_params(axis = 'both', which = 'major', labelsize = 14)
    ax.set_xlim(0,) 
    ax.set_ylim(0,) 
    
    fig.tight_layout()
    figname = filenames[i]
    fig.savefig(outpath_figures+ '\\' + figname + '.png', dpi=100, bbox_inches='tight')

#%% Boxplot median distances
median_distance_mean = data_ts['Median_distance_amygdules'].mean()
median_distance_std = data_ts['Median_distance_amygdules'].std()
fig, ax = plt.subplots(1, 1, figsize=(12, 6), dpi=200)

ax.errorbar(data_ts['Thin_section'], data_ts['Median_distance_amygdules'],
            yerr = data_ts['Distance_amygdules_std'],
            marker = 's', markersize = 9, color = 'indigo', ls = 'None')

ax.axhline(median_distance_mean, 0, 9.5, ls = '--', color = 'black', lw = 2, label = 'Mean')
ax.axhspan(median_distance_mean-median_distance_std, median_distance_mean+median_distance_std, 0, 9.5, ls = 'None', color = 'lightgrey', lw = 2, label = 'Mean')           
ax.set_ylabel(r'Median distance ($\mathregular{\mu}$m)', fontsize=18, weight = 'bold')
ax.tick_params(axis = 'both', which = 'major', labelsize = 14)
ax.set_ylim(0,) 

fig.tight_layout()
figname = 'Top_median_distances'
fig.savefig(outpath_figures+ '\\' + figname + '.png', dpi=100, bbox_inches='tight')

#%% Boxplot mean distances
mean_distance_mean = data_ts['Mean_distance_amygdules'].mean()
mean_distance_std = data_ts['Mean_distance_amygdules'].std()
fig, ax = plt.subplots(1, 1, figsize=(12, 6), dpi=200)

ax.errorbar(data_ts['Thin_section'], data_ts['Mean_distance_amygdules'],
            yerr = data_ts['Distance_amygdules_std'],
            marker = 's', markersize = 9, color = 'indigo', ls = 'None')

ax.axhline(mean_distance_mean, 0, 9.5, ls = '--', color = 'black', lw = 2, label = 'Mean')  
ax.axhspan(mean_distance_mean-mean_distance_std, mean_distance_mean+mean_distance_std, 0, 9.5, ls = 'None', color = 'lightgrey', lw = 2, label = 'Mean')       
ax.set_ylabel(r'Mean distance ($\mathregular{\mu}$m)', fontsize=18, weight = 'bold')
ax.tick_params(axis = 'both', which = 'major', labelsize = 14)
ax.set_ylim(0,) 

fig.tight_layout()
figname = 'Top_mean_distances'
fig.savefig(outpath_figures+ '\\' + figname + '.png', dpi=100, bbox_inches='tight')

#%% Plot perc area - area amygdules
colors = [ 'royalblue', 'forestgreen']
markers = ['^', '^']
lithology = ['Mng_Top', 'Mnb_Top']
color_map = dict(zip(lithology, colors))

dpi = 300  
fig, ax = plt.subplots(1, 1, figsize=(10 ,7), dpi=dpi)

for i, row in data_ts.iterrows():
    current_lith = row['Lithology']
    current_color = color_map.get(current_lith, 'grey') 
    val = row['Number_amygdules']
    current_ms = 10 + (25 - 10) * (val - 8) / (396 - 8)
    
    ax.errorbar(row['Perc_area_amygdules'], row['Area_amygdules_mean_cm2'],
                yerr = row['Area_amygdules_std_cm2'],# xerr = row['Area_amygdules_std_cm2'],
                marker = '^', markersize = current_ms, color = current_color, ls = 'None',
                mec = 'black', mew = 0.5)
legend_elements = [
    Line2D([0], [0], marker='^', color='w', label='Mng_Top',
           markerfacecolor='royalblue', markersize=12, markeredgecolor='black'),
    Line2D([0], [0], marker='^', color='w', label='Mnb_Top',
           markerfacecolor='forestgreen', markersize=12, markeredgecolor='black')
]

size_elements = [
    Line2D([0], [0], marker='^', color='w', label='< 50', 
           markerfacecolor='grey', markersize=5, markeredgecolor='black'),
    Line2D([0], [0], marker='^', color='w', label='50 - 300', 
           markerfacecolor='grey', markersize=12, markeredgecolor='black'),
    Line2D([0], [0], marker='^', color='w', label='> 300', 
           markerfacecolor='grey', markersize=20, markeredgecolor='black')
]
leg1 = ax.legend(handles=legend_elements, loc='upper left', title="Lithology", title_fontproperties={'size': 14}, 
                 fontsize=14, frameon=True, framealpha = 1)
ax.add_artist(leg1)
ax.legend(handles=size_elements, loc='upper right', title="Number of amygdules", title_fontproperties={'size': 14}, 
          fontsize=14, frameon=True, framealpha = 1)

# ax.legend(handles=legend_elements, loc='upper right', fontsize=14, frameon=True, framealpha = 1)    
ax.set_xlabel(r'Relative surface area amygdules (%)', fontsize=18, weight = 'bold')        
ax.set_ylabel(r'Amygdule area ($\mathregular{cm^2}$)', fontsize=18, weight = 'bold')
ax.tick_params(axis = 'both', which = 'major', labelsize = 14)
ax.set_xlim(0,) 
ax.set_ylim(0,) 

fig.tight_layout()
figname = 'Perc_area_area'
fig.savefig(outpath_figures+ '\\' + figname + '.png', dpi=dpi, bbox_inches='tight')
fig.savefig(outpath_figures+ '\\' + figname + '.pdf', dpi=dpi, bbox_inches='tight')

#%% Plot mean distance - diameter
colors = [ 'royalblue', 'forestgreen']
markers = ['^', '^']
lithology = ['Mng_Top', 'Mnb_Top']
color_map = dict(zip(lithology, colors))
# Define figsize to match other field data
# px_w, px_h = 858.215, 516.160
dpi = 300  
# fig_w = px_w / dpi
# fig_h = px_h / dpi

fig, ax = plt.subplots(1, 1, figsize=(10,7), dpi=dpi)

# ax.axhline(median_distance_mean, 0, 9.5, ls = '--', color = 'black', lw = 2, label = 'Mean')   
# ax.axhspan(median_distance_mean-median_distance_std, median_distance_mean+median_distance_std, 0, 9.5, ls = 'None', color = 'lightgrey', lw = 2, label = 'Mean')   
for i, row in data_ts.iterrows():
    current_lith = row['Lithology']
    current_color = color_map.get(current_lith, 'grey') 
    val = row['Number_amygdules']
    current_ms = 10 + (25 - 10) * (val - 8) / (396 - 8)
    
    ax.errorbar(row['Diameter_amygdules_mean_cm'], row['Mean_distance_amygdules_cm'],
                yerr = row['Distance_amygdules_cm_std'], xerr = row['Diameter_amygdules_std_cm'],
                marker = '^', markersize = current_ms, color = current_color, ls = 'None',
                mec = 'black', mew = 0.5)
legend_elements = [
    Line2D([0], [0], marker='^', color='w', label='Mng_Top',
           markerfacecolor='royalblue', markersize=12, markeredgecolor='black'),
    Line2D([0], [0], marker='^', color='w', label='Mnb_Top',
           markerfacecolor='forestgreen', markersize=12, markeredgecolor='black')
]

size_elements = [
    Line2D([0], [0], marker='^', color='w', label='< 50', 
           markerfacecolor='grey', markersize=5, markeredgecolor='black'),
    Line2D([0], [0], marker='^', color='w', label='50 - 300', 
           markerfacecolor='grey', markersize=12, markeredgecolor='black'),
    Line2D([0], [0], marker='^', color='w', label='> 300', 
           markerfacecolor='grey', markersize=20, markeredgecolor='black')
]
leg1 = ax.legend(handles=legend_elements, loc='upper left', title="Lithology", title_fontproperties={'size': 14}, 
                 fontsize=14, frameon=True, framealpha = 1)
ax.add_artist(leg1)
ax.legend(handles=size_elements, loc='upper right', title="Number of amygdules", title_fontproperties={'size': 14}, 
          fontsize=14, frameon=True, framealpha = 1)

# ax.legend(handles=legend_elements, loc='upper right', fontsize=14, frameon=True, framealpha = 1)    
ax.set_xlabel(r'Mean diameter amygdules (cm)', fontsize=18, weight = 'bold')        
ax.set_ylabel(r'Mean nearest neighbor distance (cm)', fontsize=18, weight = 'bold')
ax.tick_params(axis = 'both', which = 'major', labelsize = 14)
ax.set_xlim(0,) 
ax.set_ylim(0,) 

fig.tight_layout()
figname = 'Diameter_distance'
fig.savefig(outpath_figures+ '\\' + figname + '.png', dpi=dpi, bbox_inches='tight')
fig.savefig(outpath_figures+ '\\' + figname + '.pdf', dpi=dpi, bbox_inches='tight')

#%% Plot perc area - median distance
colors = [ 'royalblue', 'forestgreen']
markers = ['^', '^']
lithology = ['Mng_Top', 'Mnb_Top']
color_map = dict(zip(lithology, colors))

fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=200)

# for i in range(len(data_ts)):
#     ax.errorbar(data_ts['Perc_area_amygdules'][i], data_ts['Median_distance_amygdules'][i],
#                 yerr = data_ts['Distance_amygdules_std'],
#                 marker = '^', markersize = 11, color = 'indigo', ls = 'None')

ax.axhline(median_distance_mean, 0, 9.5, ls = '--', color = 'black', lw = 2, label = 'Mean')   
ax.axhspan(median_distance_mean-median_distance_std, median_distance_mean+median_distance_std, 0, 9.5, ls = 'None', color = 'lightgrey', lw = 2, label = 'Mean')   
for i, row in data_ts.iterrows():
    current_lith = row['Lithology']
    current_color = color_map.get(current_lith, 'grey') 
    
    ax.errorbar(row['Perc_area_amygdules'], 
                row['Median_distance_amygdules'],
                yerr = row['Distance_amygdules_std'],
                marker = '^', 
                markersize = 11, 
                color = current_color, # Applied here
                ls = 'None',
                mec = 'black', # Optional: adds a black edge for better visibility
                mew = 0.5)
legend_elements = [
    Line2D([0], [0], marker='^', color='w', label='Mng_Top',
           markerfacecolor='royalblue', markersize=12, markeredgecolor='black'),
    Line2D([0], [0], marker='^', color='w', label='Mnb_Top',
           markerfacecolor='forestgreen', markersize=12, markeredgecolor='black')
]

ax.legend(handles=legend_elements, loc='upper right', fontsize=14, frameon=True)    
ax.set_xlabel(r'Relative surface area amygdules (%)', fontsize=18, weight = 'bold')        
ax.set_ylabel(r'Median distance ($\mathregular{\mu}$m)', fontsize=18, weight = 'bold')
ax.tick_params(axis = 'both', which = 'major', labelsize = 14)
ax.set_xlim(0,) 
ax.set_ylim(0,) 

fig.tight_layout()
figname = 'Perc_area_median_distance'
fig.savefig(outpath_figures+ '\\' + figname + '.png', dpi=100, bbox_inches='tight')


#%% Plot perc area - mean distance
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=200)

for i, row in data_ts.iterrows():
    current_lith = row['Lithology']
    current_color = color_map.get(current_lith, 'grey') 
    
    ax.errorbar(row['Perc_area_amygdules'], 
                row['Mean_distance_amygdules'],
                yerr = row['Distance_amygdules_std'],
                marker = '^', 
                markersize = 11, 
                color = current_color, # Applied here
                ls = 'None',
                mec = 'black', # Optional: adds a black edge for better visibility
                mew = 0.5)
legend_elements = [
    Line2D([0], [0], marker='^', color='w', label='Mng_Top',
           markerfacecolor='royalblue', markersize=12, markeredgecolor='black'),
    Line2D([0], [0], marker='^', color='w', label='Mnb_Top',
           markerfacecolor='forestgreen', markersize=12, markeredgecolor='black')
]

ax.axhline(mean_distance_mean, 0, 9.5, ls = '--', color = 'black', lw = 2, label = 'Mean') 
ax.axhspan(mean_distance_mean-mean_distance_std, mean_distance_mean+mean_distance_std, 0, 9.5, ls = 'None', color = 'lightgrey', lw = 2, label = 'Mean')    
ax.legend(handles=legend_elements, loc='upper right', fontsize=14, frameon=True)  
ax.set_xlabel(r'Relative surface area amygdules (%)', fontsize=18, weight = 'bold')        
ax.set_ylabel(r'Mean distance ($\mathregular{\mu}$m)', fontsize=18, weight = 'bold')
ax.tick_params(axis = 'both', which = 'major', labelsize = 14)
ax.set_xlim(0,) 
ax.set_ylim(0,) 

fig.tight_layout()
figname = 'Perc_area_mean_distance'
fig.savefig(outpath_figures+ '\\' + figname + '.png', dpi=100, bbox_inches='tight')


#%% Export data

data_ts.to_csv(r'C:\Users\jmarggra\Documents\Articles\Erosion_meas_methods\Data\Data_thin_sections.csv') 









