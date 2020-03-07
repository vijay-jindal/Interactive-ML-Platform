import environmentVariable


def getHyperparameters(algorithm_name):

    if "Random_Forest" == algorithm_name:
        return environmentVariable.Algorithm.random_forest

    elif "Support_Vector_Machine" == algorithm_name:
        return environmentVariable.Algorithm.support_vector_machine

    elif "K_Nearest_Neighbour" == algorithm_name:
        return environmentVariable.Algorithm.k_nearest_neighbours

    else:
        return "Invalid Algorithm Selected"
