fittingDict = {
	"GaussCB" : {
		"Xic" : {
			"general" : {
				"mass_range" : [2420, 2520],
				"peak_range" : [2469, 2450, 2485],
				
				"normalisation_factor" : 0.01,
				"exponential_normalisation_factor" : 0.001,
				
				"exponential_range" : [-0.002, -8, 0],
				
				"width_range" : [6, 3, 25],
				
				"cb_width_range" : [6, 1, 25],
				"cb_alpha_range" : [24,0,25.0],
				"cb_n_range" : [9.0,0.0,10.0]
			}
		},
			
		"Lc" : {
			"general" : {
				"mass_range" : [2240, 2340],
				"peak_range" : [2290,2260,2305],
				
				"normalisation_factor" : 0.01,
				"exponential_normalisation_factor" : 0.05,
				
				"exponential_range" : [-0.001, -3,0],
				
				"width_range" : [6,3,25],
				
				"cb_width_range" : [20,1,15],
				"cb_alpha_range" : [1.0,0,5.0],
				"cb_n_range" : [9.0,0.0,10.0],
			}
		}
	},
	
	"Bukin" : {
		"Xic" : {
		    "general" : {
				"mass_range" : [2420, 2520],
				"peak_range" : [2469, 2455, 2485],
				
				"normalisation_factor" : 0.1,
				"exponential_normalisation_factor" : 0.1,
				
				"exponential_range" : [-0.0002, -2, 2],

				"Bukin_Xp_range" : [2471, 2450, 2500],
				"Bukin_Sigp_range" : [13.01, 2, 15],
				"Bukin_xi_range" : [-0.306, -0.5, 0.5],
				"Bukin_rho1_range" : [-0.853, -0.1, 0],
				"Bukin_rho2_range" : [0.8, 0, 0.1],
			}
		},
		"Lc" : {
		    "general" : {
				"mass_range" : [2240, 2340],
				"peak_range" : [2290, 2260, 2305],
				
				"normalisation_factor" : 0.1,
				"exponential_normalisation_factor" : 0.1,
				
				"exponential_range" : [-0.001, -3, 0],

				"Bukin_Xp_range" : [2290, 2280, 2395],
				"Bukin_Sigp_range" : [13.01, 2, 15],
				"Bukin_xi_range" : [-0.306, -0.5, 0.5],
				"Bukin_rho1_range" : [-0.0001, -0.1, 0],
				"Bukin_rho2_range" : [0.0001, 0, 0.1],
		}
		}
	}
}
