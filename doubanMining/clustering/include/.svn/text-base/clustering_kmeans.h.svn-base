/***************************************************************************
 * 
 * Copyright (c) 2012 Baidu.com, Inc. All Rights Reserved
 * 
 **************************************************************************/
 
 
 
/**
 * @file clustering_kmeans.h
 * @author chenmingxing(com@baidu.com)
 * @date 2012/05/08 19:59:05
 * @brief The head file for kmeans clustering algorithms.
 *  
 **/




#ifndef  __CLUSTERING_KMEANS_H_
#define  __CLUSTERING_KMEANS_H_


#include "clustering_result.h"
/*******************************************************************************
 * K-Means: macros, variables, and public functions.
 ******************************************************************************/

/// Cluster Name for K-Means.
#define CLUSTER_KMEANS_NAME "kmeans"
/// Macro name for "K"
#define CLUSTER_KMEANS_K "K"
/// Macro name for "maxiter"
#define CLUSTER_KMEANS_MAXITER "maxiter"
/// Macro name for "epsilon"
#define CLUSTER_KMEANS_EPSILON "epsilon"
/// Macro name for "initmod"
#define CLUSTER_KMEANS_INITTYPE "initype"
/// Macro name for "attempts"
#define CLUSTER_KMEANS_ATTEMPTS "attempts"
/// Macro name for "distype"
#define CLUSTER_KMEANS_DISMOD "dismod"

/// The different ways for K-Means initialization
typedef enum {
    KMEANS_RANDOM_CENTERS = 1,     // Chooses random centers.
    KMEANS_PP_CENTERS = 2,         // Uses k-Means++ algorithm.
    KMEANS_MM_CENTERS = 3          // Use max-min algorithm.
} INIT_TYPE;

/// User configuration information for K-Means.
typedef struct _cluster_kmeans_conf_t {
    /// The number of cluster expected to be clustered.
    u_int K;
    /// The max iteration in one attempt of K-Means clustering.
    u_int maxiter;
    /// Expected accuracy change threshold at which the iterative algorithm stops.
    float epsilon;
    /// The flags specify the way of how to initialize the K centers.
    INIT_TYPE initype;
    /// The number of attempts to run K-Means.
    u_int attempts;
    /// Distance type used in K-Means,
    ///   0: Euclidean distance(default); 1: 1- consine.
    DISMOD_TYPE dismod;
} cluster_kmeans_conf_t;

/**
 * @Brief: User configuration file for K-Means clustering.
 * @param <IN> stream:
 *                The stream where the output contents go.
 * @param <IN> program_name:
 *                The program name.
 **/
void cluster_kmeans_usage(FILE *stream, const char *program_name);

/**
 * @Brief: Process of performing the K-Means clustering.
 * @param <IN> data:
 *                The dataset_t struct holding all the cluster data.
 * @param <IN> param:
 *                The ul_confdata_t struct holding the config information.
 * @return: a pointer to cluster_result_t: successful; NULL: error.
 **/
cluster_result_t *cluster_kmeans(dataset_t *data, ul_confdata_t *param);

#endif  //__CLUSTERING_KMEANS_H_

/* vim: set expandtab ts=4 sw=4 sts=4 tw=100: */
