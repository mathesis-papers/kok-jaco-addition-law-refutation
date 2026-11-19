import json
from math import isqrt


def golden_floor(numerator):
    return (isqrt(5 * numerator * numerator) - numerator) // 2


def outdegree(label):
    return golden_floor(label + 1)


def phi_floor(numerator):
    return numerator + golden_floor(numerator)


def partition_start(part):
    return 1 if part == 0 else phi_floor(5 * part - 1) + 3 * part


def check():
    maximum_order = 512
    endpoints = [0]
    degrees = []
    degree_rows = {}
    maxima = {}
    maximum_sets = {}
    degree_checks = 0
    for order in range(1, maximum_order + 1):
        incoming = [label for label in range(1, order) if endpoints[label] >= order]
        endpoints.append(2 * order - len(incoming))
        degrees.append(len(incoming))
        for label in incoming:
            degrees[label - 1] += 1
        assert endpoints[order] == order + outdegree(order)
        for label, degree in enumerate(degrees, 1):
            assert degree == min(label, order - outdegree(label))
            degree_checks += 1
        maxima[order] = max(degrees)
        assert maxima[order] == golden_floor(order + 2) - 1
        maximum_sets[order] = [label for label, degree in enumerate(degrees, 1)
                               if degree == maxima[order]]
        if order in [3, 4, 5, 6, 10, 11, 14, 19]:
            degree_rows[order] = list(degrees)

    assert maximum_sets[3] == [2] and maximum_sets[11] == [7]
    assert maxima[14] == 8 and maxima[3] + maxima[11] == 9
    assert maximum_sets[4] == [2, 3] and maximum_sets[10] == [6, 7]
    assert maxima[4] + maxima[10] + 1 == 9
    defect_counts = {-1: 0, 0: 0, 1: 0}
    pair_count = 0
    for first in range(3, 257):
        for second in range(first + 1, 257):
            defect = maxima[first + second] - maxima[first] - maxima[second]
            phase_floor = (golden_floor(first + second + 2) + 1
                           - golden_floor(first + 2) - golden_floor(second + 2))
            assert defect == phase_floor and defect in defect_counts
            defect_counts[defect] += 1
            pair_count += 1
    for first, second, defect in [(3, 11, -1), (3, 4, 0), (4, 6, 1)]:
        assert maxima[first + second] - maxima[first] - maxima[second] == defect

    nonrepetitive_labels = []
    for order in range(2, maximum_order):
        if outdegree(order - 1) < outdegree(order) < outdegree(order + 1):
            assert maximum_sets[order] == [outdegree(order)]
            nonrepetitive_labels.append(order)

    partition_checks = 0
    for multiplier in range(1, maximum_order // 5 + 1):
        part = 0
        while partition_start(part + 1) <= multiplier:
            part += 1
        assert partition_start(part) <= multiplier < partition_start(part + 1)
        assert maxima[5 * multiplier] == 3 * multiplier + part
        partition_checks += 1
    first_blocks = [[1, 5 * partition_start(1) - 1]]
    first_blocks.extend([5 * partition_start(part), 5 * partition_start(part + 1) - 1]
                        for part in range(1, 5))
    assert first_blocks[:3] == [[1, 44], [45, 99], [100, 154]]

    fibonacci = [0, 1]
    while fibonacci[-1] < maximum_order:
        fibonacci.append(fibonacci[-1] + fibonacci[-2])
    fibonacci_pair_count = 0
    degree_exceptions = []
    singleton_exceptions = []
    for first_index in range(4, len(fibonacci)):
        first = fibonacci[first_index]
        if first > maximum_order:
            break
        assert maxima[first] == fibonacci[first_index - 1]
        assert maximum_sets[first] == [fibonacci[first_index - 1]]
        for second_index in range(first_index, len(fibonacci)):
            second = fibonacci[second_index]
            if first + second > maximum_order:
                break
            expected = fibonacci[first_index - 1] + fibonacci[second_index - 1]
            if maxima[first + second] != expected:
                degree_exceptions.append([first, second])
            if maximum_sets[first + second] != [expected]:
                singleton_exceptions.append([first, second])
            fibonacci_pair_count += 1
    assert degree_exceptions == [[3, 3]]
    assert singleton_exceptions == [[3, 3], [5, 5]]

    original_pairs = 0
    original_degree_exceptions = []
    original_singleton_exceptions = []
    for first_index in range(5, len(fibonacci)):
        for second_index in range(4, len(fibonacci)):
            first = fibonacci[first_index]
            second = fibonacci[second_index]
            if first + second > maximum_order:
                break
            expected = fibonacci[first_index - 1] + fibonacci[second_index - 1]
            if maxima[first + second] != expected:
                original_degree_exceptions.append([first, second])
            if maximum_sets[first + second] != [expected]:
                original_singleton_exceptions.append([first, second])
            original_pairs += 1
    assert original_degree_exceptions == []
    assert original_singleton_exceptions == [[5, 5]]

    maximum_set_checks = 0
    transition_checks = 0
    corrected_morrie_checks = 0
    nested_checks = 0
    edge_progression_checks = 0
    for order in range(2, maximum_order + 1):
        prime = maxima[order]
        tail = order - prime
        endpoint = tail + outdegree(tail)
        assert maximum_sets[order] == list(range(prime, min(order, endpoint) + 1))
        assert 1 <= len(maximum_sets[order]) <= 3
        unique = len(maximum_sets[order]) == 1
        assert unique == (order == endpoints[prime]
                          and outdegree(prime + 1) == outdegree(prime) + 1)
        assert unique == (outdegree(order + 1) == outdegree(order + 2))
        if unique:
            assert endpoints[prime] == order
            assert outdegree(order) == prime
        maximum_set_checks += 1
        if order < maximum_order:
            assert (maxima[order + 1] == prime) == unique
            if unique:
                assert maximum_sets[order + 1] in [[prime, prime + 1],
                                                   [prime, prime + 1, prime + 2]]
            incoming_prime = prime - outdegree(prime)
            incoming_next = prime + 1 - outdegree(prime + 1)
            incoming_after = prime + 2 - outdegree(prime + 2)
            common = order == endpoints[prime] and incoming_next == incoming_prime
            triple = unique and maximum_sets[order + 1] == [prime, prime + 1, prime + 2]
            double = unique and maximum_sets[order + 1] == [prime, prime + 1]
            assert triple == (common and incoming_after == incoming_prime + 1)
            assert double == (common and incoming_after == incoming_prime)
            transition_checks += 1
            corrected_morrie_checks += 2
        if order + prime <= maximum_order:
            expected = order if prime == outdegree(order) else order - 1
            assert maxima[order + prime] == expected
            nested_checks += 1
        if order >= 7 and (order - 7) % 3 == 0:
            multiplier = (order - 7) // 3
            assert prime <= 4 + 2 * multiplier
            edge = endpoints[prime] >= order
            assert edge == (endpoints[prime] == order)
            edge_progression_checks += 1
    assert maximum_sets[5] == [3] and outdegree(4) == outdegree(5)
    assert maxima[19] == 11 and endpoints[11] == 18
    assert maximum_sets[4] == [2, 3] and maximum_sets[6] == [3, 4, 5]
    proposition_2_8_checks = 0
    for label in range(3, maximum_order + 1):
        singleton = maximum_sets[label - 1] == [outdegree(label) - 1]
        assert singleton == (outdegree(label) == outdegree(label + 1))
        proposition_2_8_checks += 1
    assert maximum_sets[1] == [1] and outdegree(2) != outdegree(3)
    triple_addition_checks = 0
    for first in range(1, 33):
        for second in range(1, 33):
            for third in range(1, 33):
                total = first + second + third
                defect = maxima[total] - maxima[first] - maxima[second] - maxima[third]
                phase = golden_floor(total + 2) + 2 - sum(
                    golden_floor(part + 2) for part in [first, second, third])
                assert defect == phase
                triple_addition_checks += 1
    progression_checks = 0
    for step in range(1, 33):
        coefficient = golden_floor(step)
        for multiplier in range(1, maximum_order // step + 1):
            correction = golden_floor(step * multiplier + 2) - 1 - coefficient * multiplier
            assert maxima[step * multiplier] == coefficient * multiplier + correction
            assert correction >= 0
            progression_checks += 1
    mcpherson_exhaustive_orders = 12
    explosion_subset_checks = 0
    for order in range(1, mcpherson_exhaustive_orders + 1):
        missing = [(1 << (first - 1)) | (1 << (second - 1))
                   for first in range(1, order + 1)
                   for second in range(first + 1, order + 1)
                   if endpoints[first] < second]
        minimum_explosions = order
        maximum_clique = 0
        for subset in range(1 << order):
            if all(subset & edge for edge in missing):
                minimum_explosions = min(minimum_explosions, subset.bit_count())
            if all(subset & edge != edge for edge in missing):
                maximum_clique = max(maximum_clique, subset.bit_count())
            explosion_subset_checks += 1
        assert minimum_explosions == outdegree(order) - 1
        assert maximum_clique == order - outdegree(order) + 1
    clique_interval_checks = 0
    for order in range(1, maximum_order + 1):
        largest = max(min(order, endpoints[label]) - label + 1
                      for label in range(1, order + 1))
        assert largest == order - outdegree(order) + 1
        clique_interval_checks += 1
    mcpherson_piecewise_checks = 0
    mcpherson_nonrepetition_checks = 0
    for order in range(3, maximum_order + 1):
        prime = maxima[order]
        cited_value = prime - 1 if endpoints[prime] >= order else prime
        assert cited_value == outdegree(order) - 1
        mcpherson_piecewise_checks += 1
        if order < maximum_order:
            values = [outdegree(label) - 1 for label in range(order - 1, order + 2)]
            assert (values[0] < values[1] < values[2]) == (
                outdegree(order - 1) < outdegree(order) < outdegree(order + 1))
            mcpherson_nonrepetition_checks += 1
    triple_orders = []
    index = 0
    order = 1
    while True:
        order += 3 + 2 * (golden_floor(index + 2) - golden_floor(index + 1))
        index += 1
        if order > maximum_order:
            break
        assert len(maximum_sets[order]) == 3
        triple_orders.append(order)
    assert triple_orders == [order for order in range(2, maximum_order + 1)
                             if len(maximum_sets[order]) == 3]
    order_sequence = [1] + triple_orders
    gaps = [second - first for first, second in zip(order_sequence, order_sequence[1:])]
    assert all(gap in [3, 5] for gap in gaps)
    assert all(pair != [3, 3] for pair in [gaps[index:index + 2]
                                           for index in range(len(gaps) - 1)])
    assert all(triple != [5, 5, 5] for triple in [gaps[index:index + 3]
                                                for index in range(len(gaps) - 2)])

    return {
        'status': 'pass',
        'arithmetic': 'Integer recurrence, integer square roots, and exhaustive finite comparisons.',
        'degree_checks': degree_checks,
        'maximum_order': maximum_order,
        'addition_pairs': pair_count,
        'addition_pair_domain': '3 <= n < m <= 256',
        'addition_defect_counts': {str(defect): count for defect, count in defect_counts.items()},
        'nonrepetitive_domain': '2 <= n <= 511',
        'nonrepetitive_examples': len(nonrepetitive_labels),
        'partition_multiplier_checks': partition_checks,
        'partition_initial_blocks': first_blocks,
        'fibonacci_pair_domain': 'F_r <= F_s, r,s >= 4, F_r + F_s <= 512',
        'fibonacci_pairs': fibonacci_pair_count,
        'fibonacci_degree_exceptions': degree_exceptions,
        'fibonacci_singleton_exceptions': singleton_exceptions,
        'proposition_3_2_literal_domain': 'h=F_r, r>=5; l=F_s, s>=4; h+l<=512 (the source requires F_(r-1)>=3)',
        'proposition_3_2_pairs': original_pairs,
        'proposition_3_2_degree_exceptions': original_degree_exceptions,
        'proposition_3_2_singleton_exceptions': original_singleton_exceptions,
        'maximum_set_interval_checks': maximum_set_checks,
        'maximum_set_domain': '2 <= n <= 512',
        'maximum_transition_checks': transition_checks,
        'corrected_theorem_2_3_equivalence_checks': corrected_morrie_checks,
        'theorem_2_3_counterexamples': {'part_a': {'n': 6, 'prime': 3},
                                      'part_b': {'n': 4, 'prime': 2}},
        'proposition_2_8_checks': proposition_2_8_checks,
        'proposition_2_8_excluded_boundary': 2,
        'nested_maximum_checks': nested_checks,
        'theorem_2_15_progression_checks': edge_progression_checks,
        'theorem_2_15_edge_counterexample': {'n': 19, 'maximum': 11, 'endpoint': 18},
        'triple_addition_checks': triple_addition_checks,
        'triple_addition_domain': '1 <= n1,n2,n3 <= 32',
        'arithmetic_progression_checks': progression_checks,
        'arithmetic_progression_domain': '1 <= d <= 32; k >= 1; d*k <= 512',
        'mcpherson_exhaustive_orders': mcpherson_exhaustive_orders,
        'mcpherson_explosion_subset_checks': explosion_subset_checks,
        'mcpherson_theorem_2_48_piecewise_checks': mcpherson_piecewise_checks,
        'mcpherson_theorem_2_48_domain': '3 <= n <= 512; prime maximum label; both edge cases',
        'mcpherson_nonrepetition_checks': mcpherson_nonrepetition_checks,
        'clique_interval_orders': clique_interval_checks,
        'three_maximizer_orders_checked': len(triple_orders),
        'three_maximizer_initial_orders': triple_orders[:12],
        'three_maximizer_gap_checks': len(gaps),
        'counterexample_degree_rows': {
            str(order): {
                'degrees': row,
                'maximum_degree': maxima[order],
                'maximum_labels': maximum_sets[order],
            } for order, row in degree_rows.items()
        },
        'coverage': {
            'written_proofs': 'All-order degree and multi-summand addition formulas; Lemma 2.2; progression partitions; corrected Theorems 2.3 and 2.15; neighboring implications and Fibonacci assertions. Maximum-set identities are cited from Patel (2026); the three-maximizer recurrence reformulates that classification; McPherson nonrepetition follows from Kok (2016), Theorem 2.48, and the endpoint formula.',
            'lean_declarations': 'JacoAdditionLawRefutation.result: negation of the full original addition assertion; JacoMaximumDegree.degree_formula and result: degree and maximum formulas.',
            'finite_checks': 'The explicit finite domains listed in this document.',
        },
    }


if __name__ == '__main__':
    print(json.dumps(check(), indent=2, sort_keys=True))
