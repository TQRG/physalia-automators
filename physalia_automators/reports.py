"""Reports generator for Physalia Automators experiment.

Example:
        ``$ python physalia_automators/reports.py``
"""

# pylint: disable=no-value-for-parameter
# pylint: disable=missing-docstring

import time
import csv
import click
import bisect
from collections import defaultdict
from tabulate import tabulate
from operator import itemgetter

import numpy as np
import matplotlib.pyplot as plt
from physalia.models import Measurement
from physalia.analytics import violinplot, pairwise_welchs_ttest, describe

from physalia_automators.constants import loop_count

@click.command()
@click.option('-i','--results_input', default="results.csv", type=click.Path(dir_okay=False))
@click.option('-o','--results_output', default="results", type=click.Path())
def tool(results_input, results_output):
    
    with open(results_input, 'rt') as csv_file:
        csv_reader = csv.reader(csv_file)
        data = {Measurement(*row) for row in csv_reader}
    use_case_categories = [
        "find_by_id",
        "find_by_description",
        "find_by_content",
        "tap",
        "long_tap",
        "multi_finger_tap",
        "dragndrop",
        "swipe",
        "pinch_and_spread",
        "back_button",
        "input_text",
    ]
    scores = defaultdict(lambda: 0)
    for use_case_category in use_case_categories:
        break
        click.secho("----------------------------------------", fg="blue")
        click.secho("         {}".format(use_case_category), fg="blue")
        click.secho("----------------------------------------", fg="blue")
        use_case_data = list(Measurement.get_entries_with_name_like("-"+use_case_category, data))
        unique_use_cases = list(Measurement.get_unique_use_cases(use_case_data))
        number_of_frameworks = len(unique_use_cases)
        names_dict = {
            name: name.replace("-"+use_case_category, "") for name in unique_use_cases
        }
        groups = [
            list(Measurement.get_entries_with_name(use_case, use_case_data))
            for use_case in unique_use_cases
        ]
        names = [
            name.replace("-"+use_case_category, "") for name in unique_use_cases
        ]
        names, groups = zip(*sorted(zip(names, groups)))
        title = use_case_category.title().replace('_'," ")
        violinplot(
            *groups,
            save_fig=results_output+"/"+use_case_category,
            names=names_dict, title=title, sort=True)
        n_loop_iterations = getattr(loop_count, use_case_category.upper())
        # Descriptive statistics
        table = describe(*groups, names=names, loop_count=n_loop_iterations, ranking=True)
        # Update Ranking
        for name, row in zip(names, table):
            scores[name] += (number_of_frameworks - row["Ranking"])/float(number_of_frameworks)
        # Welchs ttest
        pairwise_welchs_ttest(*groups, names=names)

    # Ranking
    # click.secho("\nRanking".format(use_case_category), fg="blue")
    # sorted_scores = sorted(scores.items(), key=itemgetter(1), reverse=True)
    # print tabulate(sorted_scores, headers=["Framework", "Score"], tablefmt="grid")
    
    frameworks=[
        "AndroidViewClient",
        "Appium",
        "Calabash",
        "Espresso",
        "Monkeyrunner",
        "PythonUiAutomator",
        "Robotium",
        "UiAutomator",
    ]
    
    for framework in frameworks:
        means = []
        for interaction in use_case_categories:
            print(framework, interaction)
            use_case = "{}-{}".format(framework, interaction)
            use_case_data = np.array(list(Measurement.get_entries_with_name(use_case, data)), dtype='float')
            if len(use_case_data):
                n_loop_iterations = getattr(loop_count, interaction.upper())
                mean = np.mean(use_case_data)/n_loop_iterations*1000
            else:
                mean = 0
            bisect.insort(
                means,
                (mean, interaction)
            )
        figure = plt.figure()
        figure.suptitle(framework)
        X = range(len(means))
        Y, names = zip(*means)
        plt.bar(X, Y)
        plt.xticks(X, names, rotation='vertical')
        for x,y in zip(X, Y):
            plt.text(x, y, '%.2f' % y, ha='center', va= 'bottom')
        figure.show()
    click.prompt("Permission to exit?")

def exit_gracefully(start_time):
    exit_time = time.time()
    duration = exit_time - start_time
    click.secho(
        "Physalia Automators reports exited in {:.4f} seconds.".format(duration),
        fg='blue'
    )

if __name__ == '__main__':
    start_time = time.time()
    try:
        tool()
    except KeyboardInterrupt:
        pass
    finally:
        exit_gracefully(start_time)
