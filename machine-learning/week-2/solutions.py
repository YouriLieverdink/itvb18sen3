import numpy as np
import matplotlib.pyplot as plt
import time
import math
from scipy.sparse import csr_matrix

# ==== OPGAVE 1 ====


def plot_number(nrVector):
    # Let op: de manier waarop de data is opgesteld vereist dat je gebruik maakt
    # van de Fortran index-volgorde – de eerste index verandert het snelst, de
    # laatste index het langzaamst; als je dat niet doet, wordt het plaatje
    # gespiegeld en geroteerd. Zie de documentatie op
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.reshape.html
    """
        Hieronder zetten we de vector om in een matrix van 20 bij 20. De laatste parameter, 'F' is
        hierbij het belangrijkst. Deze geeft aan hoe de waarden uit het 'geheugen' moeten worden
        gelezen.

        # 1. Dit is het figuur waar mee we beginnen.
        [
            [1, 1, 1],
            [1, 0, 0],
            [1, 1, 1],
        ]

        # 2. Alle kolommen van dit figuur worden onder elkaar geplakt om één vector te krijgen.
        [
            [1],
            [1],
            [1],
            [1],
            [0],
            [1],
            [1],
            [0],
            [1],
        ]

        # 3. Deze vector wordt vervolgens getransponeerd en dan is het uiteindelijke resultaat dit:
        [
            [1, 1, 1, 1, 0, 1, 1, 0, 1],
        ]

        i -  0  1  2  3  4  5  6  7  8
        De indexen om het volgende stuk iets begrijpelijker te maken.

        # 4. Om deze waarden vervolgens weer goed te krijgen zoals het figuur in # 1 moeten we de
        elementen op een 'column-major' manier worden gelezen. Dit houdt in dat er per kolom
        elementen uit de lijst worden gehaald. We beginnen bij index 0, daarna doen we + n om de
        index van de start van de volgende kolom te krijgen. Dit doen we totdat we n waarden hebben
        bereikt en dan gaan we door naar de volgende kolom. Als we dit uitvoeren voor bovenstaande
        lijst krijg je deze indexen:

        0 3 6
        1 4 7
        2 5 8

        # 5. De waarden kunnen vervolgens invullen door de vector uit # 3. te pakken en dan zien we
        dat het figuur hetzelfde is als uit # 1.

        1 1 1
        1 0 0
        1 1 1
    """
    matrix = np.reshape(nrVector, (20, 20), order='F')

    plt.matshow(matrix, cmap='Greys')
    plt.show()

# ==== OPGAVE 2a ====


def sigmoid(z):
    # Maak de code die de sigmoid van de input z teruggeeft. Zorg er hierbij
    # voor dat de code zowel werkt wanneer z een getal is als wanneer z een
    # vector is.
    # Maak gebruik van de methode exp() in NumPy.
    """
        We berekenen hier de onderkant van de functie door middel van de functie np.exp. Wat deze
        functie doet is, het kwadrateerd het getal (e) met de waarde die wordt meegegeven.
    """
    demoniator = 1 + np.exp(-z)

    return 1 / demoniator


# ==== OPGAVE 2b ====
def get_y_matrix(y, m):
    # Gegeven een vector met waarden y_i van 1...x, retourneer een (ijle) matrix
    # van m×x met een 1 op positie y_i en een 0 op de overige posities.
    # Let op: de gegeven vector y is 1-based en de gevraagde matrix is 0-based,
    # dus als y_i=1, dan moet regel i in de matrix [1,0,0, ... 0] zijn, als
    # y_i=10, dan is regel i in de matrix [0,0,...1] (in dit geval is de breedte
    # van de matrix 10 (0-9), maar de methode moet werken voor elke waarde van
    # y en m
    """
        We halen hier de maximale waarde op uit de y vector. Deze waarde bepaald namelijk de grote
        van de rijen binnen onze matrix.
    """
    n = max(y)[0]

    """
        Hier maken we een nieuwe matrix aan. Deze dimensies van deze matrix zijn gebaseerd op de
        meegegeven parameters. Deze matrix met nullen zal straks voor een deel worden gevuld met
        enen.
    """
    matrix = np.zeros((m, n))

    """
        We lopen hier door elke waarde van y heen. Dit is altijd een waarde tussen 1 en n. In de rij
        waar we nu zijn moeten we de (n)de waarde op 1 zetten. Dit betekent dus dat we 1 af moeten
        trekken van de waarde om de index te krijgen. Deze zetten we dan simpelweg op 1.
    """
    for i, v in enumerate(y):
        matrix[i][v - 1] = 1

    return matrix

# ==== OPGAVE 2c ====
# ===== deel 1: =====


def predict_number(Theta1, Theta2, X):
    # Deze methode moet een matrix teruggeven met de output van het netwerk
    # gegeven de waarden van Theta1 en Theta2. Elke regel in deze matrix
    # is de waarschijnlijkheid dat het sample op die positie (i) het getal
    # is dat met de kolom correspondeert.

    # De matrices Theta1 en Theta2 corresponderen met het gewicht tussen de
    # input-laag en de verborgen laag, en tussen de verborgen laag en de
    # output-laag, respectievelijk.

    # Een mogelijk stappenplan kan zijn:

    #    1. voeg enen toe aan de gegeven matrix X; dit is de input-matrix a1
    #    2. roep de sigmoid-functie van hierboven aan met a1 als actuele
    #       parameter: dit is de variabele a2
    #    3. voeg enen toe aan de matrix a2, dit is de input voor de laatste
    #       laag in het netwerk
    #    4. roep de sigmoid-functie aan op deze a2; dit is het uiteindelijke
    #       resultaat: de output van het netwerk aan de buitenste laag.

    # Voeg enen toe aan het begin van elke stap en reshape de uiteindelijke
    # vector zodat deze dezelfde dimensionaliteit heeft als y in de exercise.
    """ Input layer """
    a1 = X
    a1 = np.insert(a1, 0, 1, axis=1)

    """ Hidden layer """
    z2 = np.dot(Theta1, a1[:].T).T
    a2 = sigmoid(z2)
    a2 = np.insert(a2, 0, 1, axis=1)

    """ Output layer"""
    z3 = np.dot(Theta2, a2[:].T).T
    a3 = sigmoid(z3)

    return a3

# ===== deel 2: =====


def compute_cost(Theta1, Theta2, X, y):
    # Deze methode maakt gebruik van de methode predictNumber() die je hierboven hebt
    # geïmplementeerd. Hier wordt het voorspelde getal vergeleken met de werkelijk
    # waarde (die in de parameter y is meegegeven) en wordt de totale kost van deze
    # voorspelling (dus met de huidige waarden van Theta1 en Theta2) berekend en
    # geretourneerd.
    # Let op: de y die hier binnenkomt is de m×1-vector met waarden van 1...10.
    # Maak gebruik van de methode get_y_matrix() die je in opgave 2a hebt gemaakt
    # om deze om te zetten naar een matrix.
    prediction = predict_number(Theta1, Theta2, X)
    m, n = prediction.shape
    actual = get_y_matrix(y, m)

    J = 0

    for i in range(m):
        for j in range(n):

            h = prediction[i][j]
            v = actual[i][j]

            J += v * -math.log(h) + (1 - v) * -math.log(1 - h)

    return J / m

# ==== OPGAVE 3a ====


def sigmoid_gradient(z):
    # Retourneer hier de waarde van de afgeleide van de sigmoïdefunctie.
    # Zie de opgave voor de exacte formule. Zorg ervoor dat deze werkt met
    # scalaire waarden en met vectoren.
    return sigmoid(z) * (1 - sigmoid(z))

# ==== OPGAVE 3b ====


def nn_check_gradients(Theta1, Theta2, X, y):
    # Retourneer de gradiënten van Theta1 en Theta2, gegeven de waarden van X en van y
    # Zie het stappenplan in de opgaven voor een mogelijke uitwerking.

    # X.shape = (5000, 400)
    # y.shape = (5000, 1)

    # Theta1.shape = (25, 401)
    Delta2 = np.zeros(Theta1.shape)
    # Theta2.shape = (10, 26)
    Delta3 = np.zeros(Theta2.shape)

    m = X.shape[0]
    y_matrix = get_y_matrix(y, m)

    for i in range(m):
        # Forwards.
        a1 = X[i].reshape(1, 400)
        a1 = np.insert(a1, 0, 1, axis=1)

        z2 = np.dot(Theta1, a1[:].T).T
        a2 = sigmoid(z2)
        a2 = np.insert(a2, 0, 1, axis=1)

        z3 = np.dot(Theta2, a2[:].T).T
        a3 = sigmoid(z3)

        # Backwards.
        d3 = (a3 - y_matrix[i]).T  # d3.shape = (10, 1)

        grad_2 = sigmoid_gradient(z2)
        grad_2 = np.insert(grad_2, 0, 1, axis=1).T

        d2 = np.dot(Theta2.T, d3) * grad_2  # d2.shape = (26, 1)
        d2 = d2[1:, :]  # d2.shape = (25, 1)

        Delta3 = Delta3 + d3 * a2
        Delta2 = Delta2 + d2 * a1

    Delta2_grad = Delta2 / m
    Delta3_grad = Delta3 / m

    return Delta2_grad, Delta3_grad
