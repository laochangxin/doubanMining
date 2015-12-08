/***************************************************************************
 * 
 * Copyright (c) 2012 Baidu.com, Inc. All Rights Reserved
 * 
 **************************************************************************/
 
 
 
/**
 * @file clustering_result.h
 * @author chenmingxing(com@baidu.com)
 * @date 2012/05/08 20:10:23
 * @brief The declaration of the clustering result and its related functions.
 *  
 **/




#ifndef  __CLUSTERING_RESULT_H_
#define  __CLUSTERING_RESULT_H_

#include <iostream>

#include "ml_data.h"
#include "ul_conf.h"
#include "ul_log.h"

#include "clustering_utils.h"

using namespace std;

/*******************************************************************************
 * Cluster data type, and related functions.
 ******************************************************************************/
/// The cluster center information.
typedef struct _cluster_center_t {
    /// The value for each feature in this center.
    double *fea_vals;
    /// The number of feature.
    u_int fea_num;

    /// The cluster id.
    u_int cluster_id;

    /// The squared sum of each fvals in this center.
    double squared_sum;

    /// The ids of instances that belong to this cluster.
    u_int *members;
    /// The number of instances in this cluster.
    u_int mem_num;
} cluster_center_t;

/// Result of cluster informations.
typedef struct _cluster_result_t {
    /// Cluster method name
    const char *cluster_name;
    /// The distance type: 1: euclidean distance, 2: 1 - consine distance
    DISMOD_TYPE dismod;
    /// Number of original instances in training set.
    u_int ins_num;
    /// Number of original features in training set.
    u_int fea_num;
    /// Number of output clusters.
    u_int K;
    /// 1D array: [ins_num], contains the cluster index for each row.
    u_int *membership;

    /// centers[k]: contains k cluster centers.
    cluster_center_t *centers;
} cluster_result_t;

/**
 * @Brief: Copy cluster_center_t struct from src to dist.
 * @param <IN/OUT> dist:
 *                An array containing K cluster_center_t, destination.
 * @param <IN> src:
 *                An array containing K cluster_center_t, source.
 * @param <IN> K:
 *                The number of clusters, also the length of array src and dist.
 * @return: 0: success; -1: error.
 **/
int copy_centers_fvals(cluster_center_t *dist, const cluster_center_t *src,
  u_int K);

/**
 * @Brief: Determine members in each cluster using each instance's membership.
 * @param <IN/OUT> result:
 *                A pointer to cluster_result_t.
 * @return: 0: success; -1: error.
 **/
int determine_cluster_members(cluster_result_t *result);

/**
 * @Brief: Malloc the memory for an array of cluster_center_t.
 * @param <IN> K:
 *                The number of clusters.
 * @param <IN> fea_num:
 *                The number of unique features.
 * @param <IN> mem_num:
 *                The number of member instances belong to this cluster.
 * @return: a pointer to cluster_center_t: success; NULL: error.
 **/
cluster_center_t *malloc_centers(u_int K, u_int fea_num, u_int mem_num);

/**
 * @Brief: Free the memory for an array of cluster_center_t.
 * @param <IN/OUT> centers:
 *                The array containing the K cluster_center_t elements,
 *                   waiting for free.
 * @param <IN> K:
 *                The number of clusters, length of centers.
 **/
void free_centers(cluster_center_t *&centers, u_int K);

/**
 * @Brief: Malloc the memory for cluster_result_t structure.
 * @param <IN> ins_num:
 *                The number of instances.
 * @param <IN> fea_num:
 *                The number of unique features.
 * @param <IN> K:
 *                The number of clusters.
 * @return: a pointer to cluster_result_t: success; NULL: error.
 **/
cluster_result_t *malloc_cluster_result(u_int ins_num, u_int fea_num, u_int K);

/**
 * @Brief: Free the memory of cluster_result_t struct.
 * @param <IN/OUT> result:
 *                The cluster_result_t waiting for free.
 **/
void free_result(cluster_result_t *&result);

#endif  //__CLUSTERING_RESULT_H_

/* vim: set expandtab ts=4 sw=4 sts=4 tw=100: */
