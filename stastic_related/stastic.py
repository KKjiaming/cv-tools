import matplotlib.pyplot as plt
import random

def draw_distribution_picture(untracked_area,tracked_area, density = False):
    
    selected_tacked = [area for area in tracked_area if area <30000 ]
    selected_untracked = [area for area in untracked_area if area <30000 ]
    sample_selected_untracked = random.sample(selected_untracked, len(selected_tacked))
    
    plt.hist(selected_tacked,bins = 100,color="#FF0000",edgecolor='b',alpha=.9)
    # plt.savefig("tools/selected_tacked.png")
    # plt.figure()
    plt.hist(sample_selected_untracked,bins = 100,color="#C1F320",edgecolor='b',alpha=.5)
    plt.savefig("tools/selected_untracked.png")    
    
    print(f'the len of selected_tacked is {len(selected_tacked)}')
    print(f'the len of selected_untracked is {len(selected_untracked)}')
    print(f'the len of sample_selected_untracked is {len(sample_selected_untracked)}')

    plt.title("Tracked bbox and untracked bbox area distribution")
    plt.xlabel('bbox area')
    plt.ylabel('bbox number ')
    plt.legend(['tracked','untracked'])
    plt.savefig("tools/join_picture_amount-dikaer.png")
    
    return 

import seaborn as sns
def draw_descartes_products(x,y,save_path):
    
    # draw Descartes products
    with sns.axes_style("dark"):
        sns.jointplot(x, y , kind="hex")
    plt.savefig(save_path)
    
    return     