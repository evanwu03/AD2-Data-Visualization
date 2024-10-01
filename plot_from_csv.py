import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_oscilloscope(df, params):
    # Extract x and y data (first column as x, second and third columns as y1 and y2)
    x_data = df.iloc[:, 0]
    y1_data = df.iloc[:, 1]
    y2_data = df.iloc[:, 2]

    # Check if there's a third waveform for "Math 1 (A)"
    if df.shape[1] > 3:
        y3_data = df.iloc[:, 3]
        y3_label_from_header = df.columns[3]
    else:
        y3_data = None
        y3_label_from_header = None

    # Get column names (assuming the first row after skipped lines is the header)
    x_label_from_header = df.columns[0]
    y1_label_from_header = df.columns[1]
    y2_label_from_header = df.columns[2]


    # Create the plot
    fig, ax = plt.subplots()

    # Get the plot colors from params, defaulting to orange and blue if not provided
    color_1 = params.get('color_1', 'orange')
    color_2 = params.get('color_2', 'blue')
    color_3 = params.get('color_3', 'red')  # For custom channels

    # Plot both curves: x vs y1 and x vs y2
    ax.plot(x_data, y1_data, color=color_1, label=y1_label_from_header)
    ax.plot(x_data, y2_data, color=color_2, label=y2_label_from_header)

    # Plot Math 1 (A) if the third waveform exists
    if y3_data is not None:
        ax.plot(x_data, y3_data, color=color_3, label=y3_label_from_header)

    # Set title from params (or default to "Graph")
    ax.set_title(params.get('title', 'Graph'))

    # Set axis labels using headers for x-axis and 'Voltage (V)' for y-axis
    ax.set_xlabel(x_label_from_header)
    ax.set_ylabel('Voltage (V)')

    # Set axis ranges if provided
    if 'x_range' in params:
        ax.set_xlim(params['x_range'])
    if 'y_range' in params:
        ax.set_ylim(params['y_range'])

    # Set ticks for x and y axes
    if 'x_ticks' in params:
        ax.locator_params(axis='x', nbins=params['x_ticks'])
    if 'y_ticks' in params:
        ax.locator_params(axis='y', nbins=params['y_ticks'])

    # Add grid
    ax.grid(True, which='both', linestyle='--', linewidth=0.7)

    # Show the legend for both plots
    ax.legend(loc='upper right')

    return fig

def plot_network_analyzer(df, params):
    # Extract data
    freq_data = df.iloc[:, 0]
    ch1_mag_data = df.iloc[:, 1]
    ch2_mag_data = df.iloc[:, 2]
    ch2_phase_data = df.iloc[:, 3]

    # Get column names
    freq_label_from_header = df.columns[0]
    ch1_mag_label_from_header = df.columns[1]
    ch2_mag_label_from_header = df.columns[2]
    ch2_phase_label_from_header = df.columns[3]

    # Create the figure and subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Get the plot colors from params, defaulting to orange and blue if not provided
    color_ch1_mag = params.get('color_ch1_mag', 'orange')
    color_ch2_mag = params.get('color_ch2_mag', 'blue')
    color_ch2_phase = params.get('color_ch2_phase', 'red')

    # Plot frequency vs magnitude for Channel 1 and Channel 2
    ax1.plot(freq_data, ch1_mag_data, color=color_ch1_mag, label=ch1_mag_label_from_header)
    ax1.plot(freq_data, ch2_mag_data, color=color_ch2_mag, label=ch2_mag_label_from_header)
    ax1.set_title('Magnitude')
    ax1.set_xlabel(freq_label_from_header)
    ax1.tick_params(labelbottom='Visible')
    ax1.set_ylabel('Magnitude (X)')
    ax1.legend(loc="upper right")

    # Set x-axis to log scale
    ax1.set_xscale('log')

    # Set axis ranges and ticks if provided
    if 'xlims' in params:
        ax1.set_xlim(params['xlims'])
    if 'ylims_mag' in params:
        ax1.set_ylim(params['ylims_mag'])
    if 'xticks' in params:
        ax1.locator_params(axis='x', nbins=params['xticks'])
    if 'yticks_mag' in params:
        ax1.locator_params(axis='y', nbins=params['yticks'])

    # Add grid to magnitude plot
    ax1.grid(True, which='both', linestyle='--', linewidth=0.7)

    # Plot frequency vs phase for Channel 2
    ax2.plot(freq_data, ch2_phase_data, color=color_ch2_phase, label=ch2_phase_label_from_header)
    ax2.set_title('Phase')
    ax2.set_xlabel(freq_label_from_header)
    ax2.set_ylabel('Phase (deg)')
    ax2.legend(loc="upper right")

    # Set x-axis to log scale
    ax2.set_xscale('log')

    # Set axis ranges and ticks if provided
    if 'xlims' in params:
        ax2.set_xlim(params['xlims'])
    if 'ylims_phase' in params:
        ax2.set_ylim(params['ylims_phase'])
    if 'xticks' in params:
        ax2.locator_params(axis='x', nbins=params['xticks'])
    if 'yticks_phase' in params:
        ax2.locator_params(axis='y', nbins=params['yticks'])

    # Add grid to phase plot
    ax2.grid(True, which='both', linestyle='--', linewidth=0.7)

    # Adjust spacing between subplots
    plt.tight_layout()

    return fig

def plot_impedance_analyzer(df, params):
    # Extract data
    freq_data = df.iloc[:, 0]
    trace_th_data = df.iloc[:, 1]
    trace_rs_data = df.iloc[:, 2]
    trace_xs_data = df.iloc[:, 3]

    # Get column names
    freq_label_from_header = df.columns[0]
    trace_th_label_from_header = df.columns[1]
    trace_rs_label_from_header = df.columns[2]
    trace_xs_label_from_header = df.columns[3]

    # Create the figure and subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Get the plot colors from params
    color_trace_rs = params.get('color_trace_rs', 'orange')
    color_trace_xs = params.get('color_trace_xs', 'blue')
    color_trace_th = params.get('color_trace_th', 'red')

    # Plot frequency vs Trace Rs and Trace Xs
    ax1.plot(freq_data, trace_rs_data, color=color_trace_rs, label=trace_rs_label_from_header)
    ax1.plot(freq_data, trace_xs_data, color=color_trace_xs, linestyle='--', label=trace_xs_label_from_header)
    ax1.set_title('Resistance (Rs) and Reactance (Xs) vs Frequency')
    ax1.set_xlabel(freq_label_from_header)
    ax1.set_ylabel('Resistance/Reactance (Ohm)')
    ax1.legend()

    # Set x-axis to log scale
    #ax1.set_xscale('log')

    # Set axis ranges and ticks if provided
    if 'xlims' in params:
        ax1.set_xlim(params['xlims'])
    if 'ylims_rs_xs' in params:
        ax1.set_ylim(params['ylims_rs_xs'])
    if 'xticks' in params:
        ax1.xaxis.set_major_locator(plt.LogLocator(base=10.0, numticks=params['xticks']))
    if 'yticks_rs_xs' in params:
        ax1.yaxis.set_major_locator(plt.MaxNLocator(params['yticks_rs_xs']))

    # Add grid to resistance/reactance plot
    ax1.grid(True, which='both', linestyle='--', linewidth=0.7)

    # Plot frequency vs Trace th
    ax2.plot(freq_data, trace_th_data, color=color_trace_th, label=trace_th_label_from_header)
    ax2.set_title('Phase vs Frequency')
    ax2.set_xlabel(freq_label_from_header)
    ax2.set_ylabel('Phase (deg)')
    ax2.legend()

    # Set x-axis to log scale
    ax2.set_xscale('log')

    # Set axis ranges and ticks if provided
    if 'xlims' in params:
        ax2.set_xlim(params['xlims'])
    if 'ylims_th' in params:
        ax2.set_ylim(params['ylims_th'])
    if 'xticks' in params:
        ax2.xaxis.set_major_locator(plt.LogLocator(base=10.0, numticks=params['xticks']))
    if 'yticks_th' in params:
        ax2.yaxis.set_major_locator(plt.MaxNLocator(params['yticks_th']))

    # Add grid to phase plot
    ax2.grid(True, which='both', linestyle='--', linewidth=0.7)

    # Adjust spacing between subplots
    plt.tight_layout()

    return fig

def plot_curve_trace(df, params):
    # Extract x and y data (first column as x, second and third columns as y1 and y2)
    voltage = df.iloc[:, 0]
    current = df.iloc[:, 1]

    # Create the plot
    fig, ax = plt.subplots()

    # Get the plot colors from params, defaulting to orange and blue if not provided
    color_1 = params.get('color_1', 'red')

    # Plot both curves: x vs y1 and x vs y2
    ax.scatter(voltage, current, color=color_1, linewidths=0.1)

    # Set title from params (or default to "Graph")
    ax.set_title(params.get('title', 'Graph'))

    # Set axis labels using headers for x-axis and 'Voltage (V)' for y-axis
    ax.set_xlabel('Voltage (V)')
    ax.set_ylabel('$I_C$ (A)')

    # Set axis ranges if provided
    if 'x_range' in params:
        ax.set_xlim(params['x_range'])
    if 'y_range' in params:
        ax.set_ylim(params['y_range'])

    # Set ticks for x and y axes
    if 'x_ticks' in params:
        ax.locator_params(axis='x', nbins=params['x_ticks'])
    if 'y_ticks' in params:
        ax.locator_params(axis='y', nbins=params['y_ticks'])

    # Add grid
    ax.grid(True, which='both', linestyle='--', linewidth=0.7)

    # Show the legend for both plots
    #ax.legend(loc='upper right')

    return fig

def plot_from_csv(filename, params):
    try:
        # Open the file and determine how many rows to skip
        skip_rows = 0

        with open(filename, 'r', encoding='ANSI', newline='\n') as csv_file:
            for row in csv_file:
                if row.startswith('#') or row.isspace():
                    skip_rows += 1
                else:
                    break

        # Load data from the CSV file, skipping descriptive and empty rows
        df = pd.read_csv(filename, encoding='ANSI', skiprows=skip_rows)

        # Check device type and call the appropriate plotting function
        device = params.get('device')
        if device == 'oscilloscope':
            fig = plot_oscilloscope(df, params)
        elif device == 'network_analyzer':
            fig = plot_network_analyzer(df, params)
        elif device == 'impedance_analyzer':
            fig = plot_impedance_analyzer(df, params)
        elif device == 'curve_trace':
            fig = plot_curve_trace(df,params)
        else:
            raise ValueError("Unsupported device type. Please use 'oscilloscope' or 'network_analyzer'.")

        # Save the plot if 'save_path' is provided in params
        save_path = params.get('save_path')
        if save_path:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            # Save the plot
            plt.savefig(save_path)
            print(f"Plot saved to {save_path}")

        # Enable interactive features (zooming and panning)
        plt.show()

    except FileNotFoundError:
        print(f"Error: The file {filename} does not exist.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def user_interface():
    while True:
        filename = input("Enter the path to the CSV file (or 'q' to quit): ").strip()
        if filename.lower() == 'q':
            print("Exiting the program.")
            break
        elif not os.path.exists(filename):
            print("File does not exist")
            continue


        device = input("Enter the device name (oscilloscope, network_analyzer, impedance_analyzer, curve_trace): ").strip().lower()
        if device not in ['oscilloscope', 'network_analyzer', 'impedance_analyzer', 'curve_trace']:
            print("Error: Device not found. Please enter a valid device name.")
            continue

        plot_name = input("Enter the name of the plot: ").strip()
        save_directory = input("Enter the directory to save the plot: ").strip()

        params = {
            'device': device,
            'title': plot_name,
            'save_path': os.path.join(save_directory, f"{plot_name}.png")
        }

        plot_from_csv(filename, params)

def main():
    user_interface()

if __name__ == "__main__":
    main()
