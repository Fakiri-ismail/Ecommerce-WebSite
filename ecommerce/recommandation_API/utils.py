
import csv

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform

from store.models import Product, Review

def extract_csv():
    products = Product.objects.all()
    reviews = Review.objects.all()

    p = csv.writer(open('Products.csv', 'w'), lineterminator='\n')
    p.writerow(['productId', 'title', 'category', 'price', 'quantity'])

    for product in products:
        p.writerow([product.id, product.title, product.category, product.price, product.quantity])

    r = csv.writer(open('Reviews.csv', 'w'), lineterminator='\n')
    r.writerow(['customer', 'productId', 'rating'])

    for review in reviews:
        r.writerow([review.customer.id, review.product.id, review.rating])


#------GLOBAL VARIABLES-------
#---READ CSV FILES---
df_ratings = pd.read_csv(
    'Reviews.csv',
    usecols=['customer', 'productId', 'rating'],
    dtype={'customer': 'int32', 'productId': 'int32', 'rating': 'float32'})

df_products = pd.read_csv(
    'Products.csv',
    usecols=['productId', 'title'],
    dtype={'productId': 'int32', 'title': 'str'})

#---product_user Matrix---
product_user_mat = df_ratings.pivot(index='productId', columns='customer', values='rating').fillna(0)

def cosine_sim(X, Y):
    c=0; rx=0; ry=0
    if len(X) == len(Y):
        for i in range(len(X)):
            c += X[i]*Y[i] 
            rx += X[i]**2
            ry += Y[i]**2
        return c / ((rx*ry)**0.5)

#---similarity_products Matrix---
dists = pdist(product_user_mat, cosine_sim)
sim_Mtx = pd.DataFrame(squareform(dists), columns=product_user_mat.index, index=product_user_mat.index)

def productTitle(productId):
    for ligne in df_products.values:
        if ligne[0]==productId:
            return ligne[1]

def makeRecommandation(n_rec, userId):
    # identify the products rated and norated by user
    for idUser, ligne in product_user_mat.T.iterrows():
        if idUser == userId:
            combine_PrdId_Rat = list(zip(ligne.index, ligne.values))   # [(productid, rating),....]
            rated = [prdId for prdId, rat in combine_PrdId_Rat if rat !=0 ]
            norated = [prdId for prdId, rat in combine_PrdId_Rat if rat ==0 ]
        else:
            continue

    # liste des Prédictions de rating pour les produits non evalué par l'utilistater 'userId'
    R=[]
    for noratedPrdtId in norated:
        S1=0; S2=0
        for ratedPrdtId in rated:
            r=product_user_mat[userId][ratedPrdtId]
            S1 += sim_Mtx[noratedPrdtId][ratedPrdtId]*r
            S2 += sim_Mtx[noratedPrdtId][ratedPrdtId]
        if S2 == 0:
            ri = 0
        else:
            ri = S1 / S2
        R.append((noratedPrdtId, ri))
        
    # trier la liste
    for i in range(len(R)-1):
        for j in range(i,len(R)):
            if R[i][1]<R[j][1]:
                ECH=R[i]
                R[i]=R[j]
                R[j]=ECH
    
    #affichage de 'n_prdtRec' produits
    print(f"Les {n_rec} produits recommandé  pour l'utilisateur {userId} :")
    for prdId, rating in R[:n_rec]:
        title = productTitle(prdId)
        print(f'{title} avec un rating = {rating}')
    
    return R[:n_rec]