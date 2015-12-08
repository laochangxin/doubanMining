/***************************************************************************
 * 
 * Copyright (c) 2012 Baidu.com, Inc. All Rights Reserved
 * 
 **************************************************************************/
 
 
 
/**
 * @file CKMHCLUST.h
 * @author dongdaxiang@baidu.com
 * @date 2012/11/28 19:58:33
 * @brief The declaration of functions used for CKMHCLUST_client
 *  
 **/


#ifndef CKMHCLUST_AD_H_
#define CKMHCLUST_AD_H_

/**
 * @Brief: Hierachical clustering header file
 * @param <IN> unsigned level, maximum level of hierachy
 * @param <IN> unsigned split, how many folds are splitted on each subcluster 
 * @param <IN> double threshold_energy, stopping criteria for splitting,
 *             when mean distance is smaller than threshold_energy, stop splitting nodes
 * @param <IN> char * input_file, input data file
 # @param <IN> char * model_folder, output model folder path
 * @return: 0: success; -1: error
 **/
extern int CKM_hclust_learn_sparse_model(unsigned level, unsigned split, double threshold_energy, \
                                         char * input_file, char * model_folder);

/**
 * @Brief: Estimate mean data distance, max data distance, min data distance value
 * @param <IN> char * input_file, input data file name
 * @param <IN> unsigned samples, number of data samples for evaluating mean, max, min value.
 * @param <OUT> double & mean_val, mean distance of sampled instances
 * @param <OUT> double & max_val, maximum distance of sampled instances
 * @param <OUT> double & min_val, minimum distance of sampled instances
 * @param <OUT> double & median_val, median distance of sampled instances
 **/
extern int CKM_hclust_estimate_data_energy(char * input_file, unsigned samples, \
                                           double & mean_val, double & max_val, \
                                           double & min_val, double & median_val);


#endif
