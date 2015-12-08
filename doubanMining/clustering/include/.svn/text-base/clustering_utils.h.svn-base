/***************************************************************************
 * 
 * Copyright (c) 2012 Baidu.com, Inc. All Rights Reserved
 * 
 **************************************************************************/
 
 
 
/**
 * @file clustering_utils.h
 * @author chenmingxing(com@baidu.com)
 * @date 2012/05/08 19:58:54
 * @brief Some common utilities used in clustering package.
 *  
 **/




#ifndef  __CLUSTERING_UTILS_H_
#define  __CLUSTERING_UTILS_H_


#include <float.h>

#include "ml_data.h"


/// Use the cluster_center_t.
typedef struct _cluster_center_t cluster_center_t;

/// Macro for cluster algorithm, key in ul_confdata_t, eg.,"algorithm : kmeans".
#define CLUSTER_ALGO "algorithm"

/// The different distance mode: euclid, and consine (define as 1 - consine).
typedef enum {EUCLID = 1, CONSINE = 2} DISMOD_TYPE;

/******************************************************************************
 * Common utilities for mlclust package.
 *****************************************************************************/
/**
 * @Brief: Calculate the distance for two instances, a and b.
 * @param <IN> a:
 *                The first instance.
 * @param <IN> b:
 *                The second instance.
 * @param <IN> dismod:
 *                The distance type, EUCLID or COSINE.
 * @return: The value of the distance between two instances.
 **/
double caculate_dist(instance_t &a, instance_t &b, DISMOD_TYPE dismod);

/**
 * @Brief: Calculate the distance for one instance and one center, a && center.
 * @param <IN> a:
 *                The instance.
 * @param <IN> center:
 *                The cluster center.
 * @param <IN> dismod:
 *                The distance type, EUCLID or COSINE.
 * @return: The value of the distance between two instances.
 **/
double caculate_dist(instance_t &a, cluster_center_t &center, DISMOD_TYPE dismod);

/******************************************************************************
 * Miscellaneous utilities.
 *****************************************************************************/
/// Returns a random interger chosen uniformly from [0, n-1).
inline int get_random(int n) {
    int u = rand() * RAND_MAX + rand();
    return ((u % n) + n) % n;
}

/// Test if a is equal to b.
inline bool eq(double a, double b) {
    return (a - b < FLT_EPSILON) && (b - a < FLT_EPSILON);
}

/// Test if a is smaller than b.
inline bool sm(double a, double b) {
    return (b - a > FLT_EPSILON);
}

/// Test if a is smaller than b.
inline bool gr(double a, double b) {
    return (a - b > FLT_EPSILON);
}

/// Test if a is smaller or equal to b.
inline bool smOrEq(double a, double b) {
    return (a - b < FLT_EPSILON);
}

/// Test if a is greater or equal to b.
inline bool grOrEq(double a, double b) {
    return (b - a < FLT_EPSILON);
}

/// ------------------------2D Array Operations.-------------------------------
/// Copy the 2D array content from src to dist
int copy_2Darray(double **dist, double **src, u_int row, u_int col);

/// Malloc memory for 2D array with [row][col].
int malloc_2Darray(double **&a, u_int row, u_int col);

/// Free 2D array.
void free_2Darray(double **&a, u_int row);

#endif  //__CLUSTERING_UTILS_H_

/* vim: set expandtab ts=4 sw=4 sts=4 tw=100: */
