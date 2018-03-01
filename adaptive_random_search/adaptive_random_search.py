import random


def rand_in_bounds(min, max):
    return min + ((max - min) * random.random())


def objective_function(vector):
    return sum(x ** 2 for x in vector)


def random_vector(bounds):
    return [rand_in_bounds(bounds[i][0], bounds[i][1])
            for i in range(len(bounds))]


def large_step_size(iter, step_size, step_sizes, iter_mult):
    if iter > 0 and iter % iter_mult == 0:
        return step_size * step_sizes[2]
    return step_size * step_sizes[1]


def take_step(minmax, current, step_size):
    position = []
    for i in range(len(current)):
        min_ = max(minmax[i][0], current[i]-step_size)
        max_ = min(minmax[i][1], current[i]+step_size)
        position.append(rand_in_bounds(min_, max_))
    return position


def take_steps(bounds, current, step_size, big_stepsize):
    step = dict()
    big_step = dict()
    step['vector'] = take_step(bounds, current['vector'], step_size)
    step['cost'] = objective_function(step['vector'])
    big_step['vector'] = take_step(bounds, current['vector'], big_stepsize)
    big_step['cost'] = objective_function(big_step['vector'])
    return step, big_step


def search(max_iter, bounds, step_sizes, iter_mult, max_iter1):
    step_size = (bounds[0][1] - bounds[0][0]) * step_sizes[0]
    current = dict()
    count = 0
    current['vector'] = random_vector(bounds)
    current['cost'] = objective_function(current['vector'])
    for i in range(max_iter):
        big_stepsize = large_step_size(i, step_size, step_sizes, iter_mult)
        # Get the regular and large step size
        step, big_step = take_steps(bounds, current, step_size, big_stepsize)
        # Compare the costs
        if step['cost'] <= current['cost'] or \
                big_step['cost'] <= current['cost']:
            count = 0
            if big_step['cost'] <= current['cost']:
                step_size, current = big_stepsize, big_step
            else:
                current = step
        else:
            count += 1
            if count >= max_no_impr:
                count = 0
                step_size = step_size / step_sizes[1]
        print("> iteration {}, best {}".format(i+1, current['cost']))
    return current


if __name__ == '__main__':
    problem_size = 2
    bounds = [[-5, 5]] * problem_size

    # algorithm configuration
    max_iter = 1000
    step_sizes = [0.05, 1.3, 3.0]  # initial/small/large step size
    iter_mult = 10  # 1 in *iter_mul* iterations, use the largest step size
    max_no_impr = 30  # early stop when no improvement

    best = search(max_iter, bounds, step_sizes, iter_mult, max_iter)
    print(best)
