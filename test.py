filter_non_xi = lambda lst: [s for s in lst if not (s.startswith('X') and s[1:].isdigit())]


print(filter_non_xi(['hello', 'X1', 'world', 'X22', 'test', 'X', 'X123']))



from rich.table import Table
from rich.console import Console

def footer(self, simutil):
    """
    Generates the footer for the log file, including total simulation time, 
    a message indicating that the simulation has ended, and iteration tables.
    """
    filter_non_xi = lambda lst: [s for s in lst if not (s.startswith('X') and s[1:].isdigit())]

    self.log("--------------------------------------------------------------------------------------------------------------------------")
    tf_sim = dp.time.time()
    self.log(f"Total Simulation Time    {'= '.rjust(67, ' ')}{str((tf_sim - dp.tinit_sim).__round__(3)/60)} minutes.")
    self.log("--------------------------------------------------------------------------------------------------------------------------\n")
    self.log(dp.figlet_format("SIMULATION  ENDED", width=100))
    self.log("--------------------------------------------------------------------------------------------------------------------------")

    if dp.JSON['parallel']:
        self.log(dp.figlet_format("SIMULATION  ITERATIONS", width=150))
        self.log("--------------------------------------------------------------------------------------------------------------------------")

        # Create a rich console with recording enabled but no live print
        console = Console(record=True, file=None)
        table = Table(show_header=True, header_style="bold cyan", border_style="bright_black")

        sweep_names = filter_non_xi(dp.JSON['sweepNames'])
        table.add_column("Iteration", justify="center", style="bold magenta")

        for name in sweep_names:
            table.add_column(name, justify="center")

        # Fill rows
        for i, values in enumerate(simutil.Map):
            vals = [str(v) for v in values[:len(sweep_names)]]
            table.add_row(str(i + 1), *vals)

        # Render table as plain text (no colors, no console print)
        rendered = console.export_text(clear=False, styles=False)

        # Log table to your file
        self.log(rendered)

    self.copyfiles()
