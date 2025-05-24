import sys



# make a test one column df

import pandas as pd 

df = pd.DataFrame({
    '23': [1, 3, 4, 5, 1, 5, 6, 5, 1, 4],
    '29': [5, 1, 5, 6, 5, 1, 4, 1, 1, 4],
    '86': [0, 0, 0, 0, 1, 0, 0, 2, 0, 0],
    '87': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    '88': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    })

print(df.to_string())


count_columns_list = []
cluster_columns_list = []
output_df = pd.DataFrame()
columns_list = df.columns.tolist()

for col in columns_list:
    # Example operations:
    # 1. Print column name and summary stats
    print(f"Column: {col}")


    # Remove 'col' from df and save as a new DataFrame
    temp_df = pd.DataFrame(df.pop(col))
    # rename to column to match the eventual cluster values
    new_col_counts = 'counts_w' + col
    count_columns_list.append(new_col_counts)
    temp_df.rename(columns={col: new_col_counts}, inplace=True)
    #print(temp_df.to_string())

    X = temp_df[[new_col_counts]]

    from sklearn.cluster import KMeans

    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(X)  # or X if you didn't standardize
    labels = kmeans.labels_  # Cluster assignment for each row
    #                          `kmeans.labels_` is a NumPy array where each entry is an 
    #                          integer (e.g., 0, 1, or 2 if you used 3 clusters) indicating 
    #                          which cluster that row belongs to

    new_col_clusters_label = 'cluster_w' + col
    # and save that new column name in a list
    cluster_columns_list.append(new_col_clusters_label)

    # get the cluster assignments and make a new column of data
    # (KMeans in scikit-learn returns cluster identifiers as integers, not strings.)
    temp_df[new_col_clusters_label] = labels

    #print(temp_df.to_string())

    # now the tricky part
    # the kmeans 'clusters' are essentially labels that don't convey relative info about the counts.
    # the small counts should get a cluster label of 'small' (also 'large', 'medium')
    # this allows cluster data to be compared week to week
    #
    # pandas df with two integer columns, 'count' and 'cluster'. a cluster can be associated with 
    # multiple counts. how to find the cluster integers associated with the smallest and largest count
    #

    unique_cluster_count = temp_df[new_col_clusters_label].nunique()
    #print("\n\n cluster count: ", unique_cluster_count, "\n\n")

    # Find the global maximum and minimum `count` values:
    max_count = temp_df[new_col_counts].max()
    min_count = temp_df[new_col_counts].min()



    print("hoser:", max_count, " ", min_count, "\n")
    # filters the DataFrame to the rows where `count` equals `max_count` and retrieves the corresponding `cluster` value
    clusters_with_max = temp_df.loc[temp_df[new_col_counts] == max_count, new_col_clusters_label].unique().tolist()
    clusters_with_min = temp_df.loc[temp_df[new_col_counts] == min_count, new_col_clusters_label].unique().tolist()

    #print(temp_df.to_string())
    print("\nmax: ", max_count, " cluster label with max: ", clusters_with_max[0], " min: ", min_count, \
        " cluster label: ", clusters_with_min[0])

    # make a copy of the clusters column for adjustment
    copy_label = new_col_clusters_label + '.copy'
    temp_df[copy_label] = temp_df[new_col_clusters_label].copy()
    #
    temp_df[copy_label] = temp_df[copy_label].replace(clusters_with_max[0], 'max')
    temp_df[copy_label] = temp_df[copy_label].replace(clusters_with_min[0], 'min')
    # Replace non-extreme values with a placeholder (e.g., NaN)
    temp_df[copy_label] = \
    temp_df[copy_label].where((temp_df[copy_label] == 'max') | (temp_df[copy_label] == 'min'), other='mid')


    if unique_cluster_count == 3:

        new_df = temp_df[[new_col_counts, new_col_clusters_label, copy_label]].copy()
        print(new_df.to_string())

        #    counts_w29  cluster_w29 cluster_w29.copy
        # 0           5            1              max
        # 1           1            0              min
        # 2           5            1              max
        # 3           6            1              max
        # 4           5            1              max
        # 5           1            0              min
        # 6           4            2              mid
        # 7           1            0              min
        # 8           1            0              min
        # 9           4            2              mid


    new_col_cl_jiggered_label = 'cluster_jiggered_w' + col
    # find the kmeans cluster identifier associated with the smallest count value





    # append those two columns to output_df 
    output_df = pd.concat([output_df, temp_df], axis=1)

    #print(output_df.to_string())




# now delete the count data columns
output_df = output_df.drop(count_columns_list, axis=1)


print(output_df.to_string()) 












