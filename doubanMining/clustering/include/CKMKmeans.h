/***************************************************************************
 * 
 * Copyright (c) 2012 Baidu.com, Inc. All Rights Reserved
 * 
 **************************************************************************/
 
 
 
/**
 * @file clustering.h
 * @author dongdaxiang@baidu.com
 * @date 2012/11/28 19:58:33
 * @brief header file for SGD Kmeans
 *  
 **/

#ifndef _CKM_KMEANS_H_
#define _CKM_KMEANS_H_
#include <vector>

//typedef char[100] strid_t;
const unsigned g_id_size = 100;
typedef unsigned uint32_t;
typedef struct CKM_model_
{
  unsigned dim; // dimension of training data, also the dimension of centers
  unsigned data_size; // instance num of training data, also the length of membership
  // model paramter
  unsigned k; // paramter k of K-means
  unsigned batch; // In mini batch mode update, we need to set batch num.
  unsigned iter; // each mini batch update is one iteration, we update centers iter times.
  // learned model 
  double ** centers; // center vector, two dimensional, center[k] is a vector of length dim
  double * center_norms; // norm of each center with length of k
  double * center_scale; // scale value of each center
  int profile_level; // timing profile level, 0 shallow profile, 1 deep profile
  //strid_t * data_strid; //
  //uint32_t * membership; //
} CKM_model_t;

/**
 * @Brief: Process of performing the Mini batch K-Means clustering.
 * @param <IN> int k:
 *                the k parameter of k means
 * @param <IN> char * datafile:
 *                dataset to be clustered
 * @param <IN> unsigned batch:
 *                batch num of learning for each epoch
 * @param <IN> unsigned learning iteration 
 * @return: a pointer to CKM_model_t, return NULL if error happened
 **/
extern CKM_model_t * CKM_Kmeans_learn_sparse_model(int k, char * datafile, unsigned batch, unsigned iter, unsigned profile);

/**
 * @Brief: free sparse model
 * @param <IN> CKM_model_t ** model:
 *                model to be freed
 * @return: a pointer to CKM_model_t, return NULL if error happened
 **/
extern int CKM_Kmeans_free_sparse_model(CKM_model_t ** model);

/**                                                                                                                                 
 * @Brief: Given a data string(should be in correct format), return the center projection value 
 * @param <IN> CKM_model_t * model:(previous generated model)
 * @param <IN> char * line, data line string
 * @param <IN> double * output_projection, should be allocated before using, length should be equal to model->k
 * @return: 0 success, -1 fail
 **/
extern int CKM_Kmeans_project_data_string_to_centers(char * line, CKM_model_t * model, double * output_projection);

#endif
