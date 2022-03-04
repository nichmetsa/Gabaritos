from cmath import pi
import numpy as np
import matplotlib.pyplot as plt
import itertools
from vpython import *


class CantedBeam:

    # resolver encontro das coordenadas elipticas

    def __init__(self, type, P, Pcoord, M, Mcoord, b, h ,L):
        
        self.b = b
        self.h = h
        self.L = L
        self.type = type
        self.radius = ((self.b/2)**2 + (self.h/2)**2)**(1/2)
        self.P = np.array(P)
        self.Pcoord = self.__is_valid_coordinate(np.array(Pcoord))
        self.M = np.array(M)
        self.Mcoord = self.__is_valid_coordinate(np.array(Mcoord))

        if self.type == 'rect':

            self.inertiay = (self.b*self.h**3)/12
            self.inertiaz = (self.h*self.b**3)/12
            self.area = self.b*self.h
        
        elif self.type == 'elpt':
            
            self.inertiay = np.pi*(self.b*self.h**3)/4
            self.inertiaz = np.pi*(self.h*self.b**3)/4
            self.area = self.b*self.h*np.pi
        
        self.inertiapolar = self.inertiay+self.inertiaz

    def tensor(self, coord):

        self.coord = self.__is_valid_coordinate(np.array(coord))

        x_P_distance = -self.coord[0,:] + self.Pcoord[0]
        y_P_distance = -self.coord[1,:] + self.Pcoord[1,:]
        z_P_distance = -self.coord[2,:] + self.Pcoord[2,:]

        sigma_x = sum(self.P[:,0]/self.area - self.P[:,1]*x_P_distance*self.coord[1,:]/self.inertiay - self.P[:,2]*x_P_distance*self.coord[2,:]/self.inertiaz - self.M[1]*self.coord[1,:]/self.inertiay - self.M[2]*self.coord[2,:]/self.inertiaz)
        sigma_y = 0
        sigma_z = 0

        radius = np.array((self.coord[1,:]**2 + self.coord[2,:]**2)**(1/2))
        seno = np.array(self.coord[1,:]/radius)
        coseno = np.array(self.coord[2,:]/radius)

        tao_xy = self.P[:,1]/self.area + sum(self.M[:,0])*radius*coseno/self.inertiapolar
        tao_xz = self.P[:,2]/self.area + sum(self.M[:,0])*radius*(-seno)/self.inertiapolar

        tao_yx = tao_xy
        tao_yz = 0

        tao_zx = tao_xz
        tao_zy = tao_yz

        self.tensor = np.array([[sigma_x,tao_xy[0],tao_xz[0]],[tao_yx,sigma_y,tao_yz],[tao_zx,tao_zy,sigma_z]])

        return self.tensor


    def __is_valid_coordinate(self, coordinates):

        if self.type == 'rect':

            if any(coordinates[0,:]>self.L):
                raise Exception('Some coordenate of P in X is out of bounds')
            if any(coordinates[0,:]<0):
                raise Exception('Some coordenate of P in X negative')
            if any(coordinates[1,:]>abs(self.h/2)):
                raise Exception('Some coordenate of P in Y is out of bounds')
            if any(coordinates[2,:]>abs(self.b/2)):
                raise Exception('Some coordenate of P in Z is out of bounds')
            return  np.array(coordinates)
        
        elif self.type == 'elpt':

            if any(coordinates[0,:]>self.L):
                raise Exception('Some coordenate of P in X is out of bounds')
            if any(coordinates[0,:]<0):
                raise Exception('Some coordenate of P in X negativa')
            
            radius = ((coordinates[2,:])**2 + (coordinates[1,:])**2)**(1/2)

            if any(radius>self.radius):
                raise Exception('Some polar coordenate of P is out of bounds')
            return  np.array(coordinates)
        
        else:
            raise Exception('Invalid section type')

class MohrsCircle:

    def __init__(self,tensor):

        self.tensor = np.array(tensor)

        self.sigma = np.array([self.tensor[0,0],self.tensor[1,1],self.tensor[2,2]]) # takes all the values in diagonal (sigmas)

        self.tao = np.array([self.tensor[0,1],self.tensor[0,2],self.tensor[1,2]]) # tau values
        
        A = np.sum(self.sigma)

        B = self.sigma[0]*self.sigma[1] + self.sigma[0]*self.sigma[2] + self.sigma[1]*self.sigma[2] - np.sum(self.tao**2)

        C = np.prod(self.sigma) + 2*np.prod(self.tao) - np.sum(self.sigma*self.tao**2)
        
        self.poly = np.array([-1,A,-B,C])

        self.roots = np.roots(self.poly)

        self.principal_stresses = self.roots[(-self.roots).argsort()] # sorts the stresses in descending order

        self.principal_stresses_combinations = np.array([list(itertools.combinations(self.principal_stresses, 2))]).reshape(3,2) # makes a matrix for the combiunation of principal stresses

        self.circle_centers = np.array(self.principal_stresses_combinations[:,0] + self.principal_stresses_combinations[:,1])/2

        self.circle_radii = np.array(self.principal_stresses_combinations[:,0] - self.principal_stresses_combinations[:,1])/2

        self.max_principal_stress = self.circle_centers + self.circle_radii

        self.min_principal_stress = self.circle_centers - self.circle_radii

    def show_data(self):

        print('data')

    def plot_data(self):
        
        colors = ['c','m','y']

        radians = np.linspace(0, 2*pi, 721)

        plt.figure(figsize=[5,5])
        plt.title('Mohrs Circle', fontsize = 18)
        plt.ylabel(r'$\tau$', fontsize = 14)
        plt.xlabel(r'$\sigma$', fontsize = 14)
        plt.axhline(color = 'k')
        plt.axvline(color = 'k')

        for i in range(0,3):

            sigma_points = self.circle_centers[i]+self.circle_radii[i]*np.cos(radians)
            tao_points = self.circle_radii[i]*np.sin(radians)
            
            'Figure size and lines'
            plt.plot(sigma_points, tao_points, label = "Mohrs' Circle", color = colors[i])
            plt.fill_between(sigma_points, tao_points, color = colors[i], alpha = 0.1)
            plt.plot([self.circle_centers[i]],[0], marker = 'o', color = colors[i])

        plt.grid()
        'Fits everything in one window'
        plt.tight_layout()
        'Show Plot'
        plt.title('Mohrs Circle', fontsize = 18)
        plt.ylabel(r'$\tau$', fontsize = 14)
        plt.xlabel(r'$\sigma$', fontsize = 14)
        plt.show()

class UnitCell:

    def __init__(self,tensor):

        self.tensor = np.array(tensor)

    def show(self):

        t = 0.001
        box(pos = vector(0.5,0,0), size = vector(t,1,1), color = vector(1,0,0))
        box(pos = vector(-0.5,0,0), size = vector(t,1,1), color = vector(1,0,0))
        box(pos = vector(0,0.5,0), size = vector(1,t,1), color = vector(0,1,0))
        box(pos = vector(0,-0.5,0), size = vector(1,t,1), color = vector(0,1,0))
        box(pos = vector(0,0,0.5), size = vector(1,1,t), color = vector(0,0,1))
        box(pos = vector(0,0,-0.5), size = vector(1,1,t), color = vector(0,0,1))

        color_gradient = abs(self.tensor)/np.max(abs(self.tensor))

        for i in range(3):
            for j in range(3):

                pos = [0,0,0]
                ori = [0,0,0]

                if self.tensor[i,j] > 0:

                    pos[i] = 0.5
                    ori[j] = 0.5
                    arrow(pos = vector(pos[0],pos[1],pos[2]), axis = vector(ori[0],ori[1],ori[2]), color = vector(color_gradient[i,j],1-color_gradient[i,j],0))

                    pos[i] = -pos[i]
                    ori[j] = -ori[j]
                    arrow(pos = vector(pos[0],pos[1],pos[2]), axis = vector(ori[0],ori[1],ori[2]), color = vector(color_gradient[i,j],1-color_gradient[i,j],0))

                elif self.tensor[i,j] < 0:

                    if i == j:

                        pos[i] = 1.0
                        ori[j] = -0.5
                        arrow(pos = vector(pos[0],pos[1],pos[2]), axis = vector(ori[0],ori[1],ori[2]), color = vector(color_gradient[i,j],1-color_gradient[i,j],0))

                        pos[i] = -pos[i]
                        ori[j] = -ori[j]
                        arrow(pos = vector(pos[0],pos[1],pos[2]), axis = vector(ori[0],ori[1],ori[2]), color = vector(color_gradient[i,j],1-color_gradient[i,j],0))

                    else:

                        pos[i] = 0.5
                        ori[j] = -0.5
                        arrow(pos = vector(pos[0],pos[1],pos[2]), axis = vector(ori[0],ori[1],ori[2]), color = vector(color_gradient[i,j],1-color_gradient[i,j],0))

                        pos[i] = -pos[i]
                        ori[j] = -ori[j]
                        arrow(pos = vector(pos[0],pos[1],pos[2]), axis = vector(ori[0],ori[1],ori[2]), color = vector(color_gradient[i,j],1-color_gradient[i,j],0))

                else:

                    continue