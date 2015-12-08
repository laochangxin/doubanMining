/***************************************************************************
 * 
 * Copyright (c) 2012 Baidu.com, Inc. All Rights Reserved
 * 
 **************************************************************************/
 
 
/**
 * @file CKMSPEC.h
 * @author dongdaxiang@baidu.com
 * @date 2012/12/26 19:58:33
 * @brief header file for CKM spectral clustering
 *  
 **/

#ifndef CKM_SPEC_H_
#define CKM_SPEC_H_

typedef struct CKM_spec_model__
{
    unsigned dim; // dimension of training data, also dim of centers
    unsigned data_size; // number of nodes in sparse graph
    unsigned k; // value of k in Kmeans and SVD
    unsigned batch; // batch value of SGDKmeans
    unsigned iter; // iteration number of SGDKmeans
    double ** centers; // center vector, two dimensional, center[k] is a vector of length dim
    double ** dataset; // G = V\SigmaU, the first k vector of V
    unsigned * membership; // membership for each node
    double * projection;  // projection for each node
    char ** dataid; // dataid, coresponding to each index of membership and projection
    int inner_profile; // profile flag, if open, loss is printed
} CKM_spec_model_t;

/**
 * @Brief: Learn a CKM_spec_model_t with a sparse graph in graphfile, value is k
 * @param <IN> int k:
 *                the k parameter of k means
 * @param <IN> char * graphfile
 *                graphfilet to be clustered
 * @return: a pointer to CKM_spec_model_t, return NULL if error happened
 **/
CKM_spec_model_t * CKM_spec_learn_sparse_graph(char * graphfile, int k);


/**
 * @Brief: free CKM_spec_model_t
 * @param <IN> CKM_spec_model_t ** model:
 *                model to be freed
 * @return: a pointer to CKM_model_t, return NULL if error happened
 **/
int CKM_spec_free_sparse_graph(CKM_spec_model_t ** model);

#endif
