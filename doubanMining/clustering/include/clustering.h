/***************************************************************************
 * 
 * Copyright (c) 2012 Baidu.com, Inc. All Rights Reserved
 * 
 **************************************************************************/
 
 
 
/**
 * @file clustering.h
 * @author chenmingxing(com@baidu.com)
 * @date 2012/05/08 19:58:33
 * @brief The declaration of functions used for clustering_tool.
 *  
 **/




#ifndef  __CLUSTERING_H_
#define  __CLUSTERING_H_

#include <getopt.h>

#include "clustering_kmeans.h"

/// Macro for buffer len.
#define BUFFER_LEN 1024

/// Macro for max key:pair in conf file.
#define MAX_CONF_ITEM 100

/******************************************************************************
 *               Declare the functions.
 ******************************************************************************/
/**
 * @Brief: User Configuration Message for Cluster Package.
 * @param <IN> program_name:
 *                The program name. 
 * @return:
 **/
void usage(const char *program_name);

/**
 * @Brief: Print the usage message for cluster algorithm.
 * @param <IN> usage_name:
 *                The certain cluster algorithm name, eg., "kmeans" or "all" to
 *                print the usage inforamtion for all cluster algorithm.
 **/
int cluster_print_usage(const char *usage_name);

/**
 * @Brief: Parser the command line information.
 * @param <IN> argc, argv[]:
 *                The command line information.
 * @param <OUT> conf_fname:
 *                The config file name for calling the clustering algorithm,
 *                    specified by flag "-c".
 * @param <OUT> data_fname:
 *                The data file name containing the cluster data,
 *                    specified by flag "-d".
 * @param <OUT> out_fname:
 *                The output file name which will be used for saving the result,
 *                   specified by flag "-o".
 * @param <OUT> is_feamap:
 *                Whether need the feature map for string typed feature,
 *                   specified by flag "-f", if specified is_feamap = true,
 *                   otherwise is_feamap = false.
 * @return: 0: success; -1: error
 **/
int cluster_parse_args(int argc, char *argv[], char *&conf_fname,
  char *&data_fname, char *&out_fname, bool &is_feamap);

/**
 * @Brief: Read config file name and convert it to ul_confdata_t.
 * @param <IN> conf_fname:
 *                The config file name for calling the clustering algorithm.
 * @return: a pointer to ul_confdata_t: successful; NULL: error
 **/
ul_confdata_t *cluster_read_conf(const char *conf_fname);

/**
 * @Brief: The main function calling the clustering algorithm.
 * @param <IN> data:
 *                The dataset_t structure containing the whole clustering data.
 * @param <IN> pconf:
 *                The ul_confdata_t structure containing the config information
 *                  for calling the clustering algorithm.
 * @return: a pointer to cluster_result_t: success;
 *          NULL: error.
 **/
cluster_result_t *cluster_exec_main(dataset_t *data, ul_confdata_t *pconf);

/**
 * @Brief: Computer the cost: cost = sum_{x_i in X} * |x_i - c_i|^2 .
 * @param <IN> data:
 *                The dataset_t structure containing the whole clustering data.
 * @param <IN> result:
 *                The resulted clusters information.
 * @param <IN/OUT> cost:
 *                The double value of cost.
 * @return: 0: success; -1: error.
 **/
int cluster_compute_cost(const dataset_t *data,
  const cluster_result_t *result, double &cost);

/**
 * @Brief: Save the clustering result information to output file.
 * @param <IN> result:
 *                The resulted clusters information.
 * @param <IN> out_fname:
 *                The output file name.
 * @return: 0: success; -1: error.
 **/
int cluster_save_result(cluster_result_t *result, const char *out_fname);

#endif  //__CLUSTERING_H_

/* vim: set expandtab ts=4 sw=4 sts=4 tw=100: */
