fittingDict = {
	"GaussCB" : {
		"Xic" : {
			"general" : {
				"mass_range" : [2420, 2520],
				"peak_range" : [2469, 2450, 2485],
				
				"normalisation_factor" : 0.1,
				"exponential_normalisation_factor" : 0.05,
				
				"exponential_range" : [-0.02, -2, 0],
				
				"width_range" : [6, 0, 25],
				
				"cb_width_range" : [6, 1, 25],
				"cb_alpha_range" : [24,0.0,25.0],
				"cb_n_range" : [9.0,0.0,10.0]
			}
		},
			
		"Lc" : {
			"general" : {
				"mass_range" : [2240, 2340],
				"peak_range" : [2290,2260,2320],
				
				"normalisation_factor" : 0.005,
				"exponential_normalisation_factor" : 0.0001,
				
				"exponential_range" : [-0.001, -0.5, 0.1],
				
				"width_range" : [6,4,20],
				
				"cb_width_range" : [17,8,50],
				"cb_alpha_range" : [1.0,0.0,20.0],
				"cb_n_range" : [9.0,0.0,10.0],
			}
		}
	},
	
	"Bukin" : {
		"Xic" : {
		    "general" : {
				"mass_range" : [2420, 2520],
				"peak_range" : [2469, 2450, 2485],
				
				"normalisation_factor" : 0.1,
				"exponential_normalisation_factor" : 0.05,
				
				"exponential_range" : [-0.02, -2, 0],
				
				"Bukin_Xp_range" : [2471, 2450, 2500],
				"Bukin_Sigp_range" : [13, 0, 15],
				"Bukin_xi_range" : [-0.3, -1, 1],
				"Bukin_rho1_range" : [-0.8, -1, 0],
				"Bukin_rho2_range" : [0.8, 0, 1],
		    }
		},
		"Lc" : {
		    "general" : {
				"mass_range" : [2240, 2340],
				"peak_range" : [2290,2260,2320],
				
				"normalisation_factor" : 0.005,
				"exponential_normalisation_factor" : 0.0001,
				
				"exponential_range" : [-0.001, -0.5, 0.1],
	    
				"Bukin_Xp_range" : [2290, 2270,  2310],
				"Bukin_Sigp_range" : [13, 5, 15],
				"Bukin_xi_range" : [-0.3, -1, 1],
				"Bukin_rho1_range" : [-0.8, -1, 0],
				"Bukin_rho2_range" : [0.8, 0, 1],
			}
		}
	}
}
