import matplotlib.pyplot as plt
import numpy as np

from pymoo.model.callback import Callback


class OneVariableOneObjectiveVisualization(Callback):

    def __init__(self,
                 do_show=True,
                 exception_if_not_applicable=True,
                 n_samples_for_surface=10000):
        super().__init__()
        self.last_pop = None
        self.do_show = do_show
        self.exception_if_not_applicable = exception_if_not_applicable
        self.n_samples_for_surface = n_samples_for_surface

    def notify(self, algorithm):
        problem = algorithm.problem

        # check whether the visualization can be done or not - throw exception or simply do nothing
        if problem.n_var > 1 or problem.n_obj > 1:
            if self.exception_if_not_applicable:
                raise Exception("This visualization can only be used for problems with one variable and one objective!")
            else:
                return

        # draw the problem surface
        xl, xu = problem.bounds()
        _X = np.linspace(xl, xu, self.n_samples_for_surface)
        _F = problem.evaluate(_X)
        plt.plot(_X, _F, label="True", color="black", alpha=0.6)
        plt.ylim(xl[0], xu[0])
        plt.ylim(_F.min(), _F.max())

        pop = algorithm.pop

        X, F, CV = pop.get("X", "F", "CV")
        plt.scatter(X[:, 0], F[:, 0], color="blue", marker="o", s=70)

        is_new = np.full(len(pop), True)
        if self.last_pop is not None:
            for k, ind in enumerate(pop):
                if ind in self.last_pop:
                    is_new[k] = False

        # plot the new population
        if is_new.sum() > 0:
            X, F, CV = pop[is_new].get("X", "F", "CV")
            plt.scatter(X[:, 0], F[:, 0], color="red", marker="*", s=70)

        if hasattr(algorithm, "off") and algorithm.off is not None:
            X, F, CV = algorithm.off.get("X", "F", "CV")
            plt.scatter(X[:, 0], F[:, 0], color="purple", marker="*", s=40)

        plt.title(f"Generation: {algorithm.n_gen}")
        plt.legend()

        if self.do_show:
            plt.show()

        # store the current population as the last
        self.last_pop = set(pop)
