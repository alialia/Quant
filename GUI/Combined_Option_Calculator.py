import tkinter as tk
from tkinter import ttk, messagebox
import math
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sys

# Black-Scholes pricing model for European call and put options
def black_scholes(S, K, T, r, sigma):
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    call_price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    put_price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    return call_price, put_price

# Calculate the Greeks for digital options
def digital_greeks(S, K, T, r, sigma, option_type='call'):
    d2 = (math.log(S / K) - (r - 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    
    delta = norm.pdf(d2) / (S * sigma * math.sqrt(T))
    vega = S * norm.pdf(d2) * math.sqrt(T)
    gamma = -norm.pdf(d2) * (d2 / (S**2 * sigma**2 * T))
    theta = -S * norm.pdf(d2) * sigma / (2 * math.sqrt(T))
    rho = -T * math.exp(-r * T) * norm.pdf(d2)
    
    if option_type == 'put':
        delta = -delta
        rho = -rho
    
    return delta, vega, gamma, theta, rho

# Calculate the Greeks for European call and put options
def greeks(S, K, T, r, sigma, option_type='call'):
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    delta_call = norm.cdf(d1)
    delta_put = norm.cdf(d1) - 1
    
    vega = S * norm.pdf(d1) * math.sqrt(T)
    
    gamma = norm.pdf(d1) / (S * sigma * math.sqrt(T))
    
    theta_call = (-S * norm.pdf(d1) * sigma / (2 * math.sqrt(T)) 
                  - r * K * math.exp(-r * T) * norm.cdf(d2))
    theta_put = (-S * norm.pdf(d1) * sigma / (2 * math.sqrt(T)) 
                 + r * K * math.exp(-r * T) * norm.cdf(-d2))
    
    rho_call = K * T * math.exp(-r * T) * norm.cdf(d2)
    rho_put = -K * T * math.exp(-r * T) * norm.cdf(-d2)
    
    if option_type == 'call':
        delta = delta_call
        theta = theta_call
        rho = rho_call
    elif option_type == 'put':
        delta = delta_put
        theta = theta_put
        rho = rho_put
    else:
        raise ValueError("Option type must be 'call' or 'put'")
    
    return delta, vega, gamma, theta, rho

# Pricing model for digital options
def digital_option(S, K, T, r, sigma, option_type='call'):
    d2 = (math.log(S / K) - (r - 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    if option_type == 'call':
        price = math.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        price = math.exp(-r * T) * norm.cdf(-d2)
    else:
        raise ValueError("Option type must be 'call' or 'put'")
    return price

# Function to calculate option prices and Greeks, and update the GUI
def calculate_option():
    try:
        S = float(entry_S.get())
        K = float(entry_K.get())
        T = float(entry_T.get())
        r = float(entry_r.get()) / 100
        sigma = float(entry_sigma.get()) / 100
        option_type = var_option_type.get()
        option_style = var_option_style.get()
        
        if option_style == 'vanilla':
            call_price, put_price = black_scholes(S, K, T, r, sigma)
            if option_type == 'call':
                price = call_price
                delta, vega, gamma, theta, rho = greeks(S, K, T, r, sigma, option_type='call')
            else:
                price = put_price
                delta, vega, gamma, theta, rho = greeks(S, K, T, r, sigma, option_type='put')
        else:
            price = digital_option(S, K, T, r, sigma, option_type)
            delta, vega, gamma, theta, rho = digital_greeks(S, K, T, r, sigma, option_type)
        
        label_price.config(text=f"{option_type.capitalize()} {option_style.capitalize()} Option Price: {price:.2f}")
        label_delta.config(text=f"Delta: {delta:.4f}")
        label_vega.config(text=f"Vega: {vega:.4f}")
        label_gamma.config(text=f"Gamma: {gamma:.4f}")
        label_theta.config(text=f"Theta: {theta:.4f}")
        label_rho.config(text=f"Rho: {rho:.4f}")
        
        plot_graphs(S, K, T, r, sigma, option_type, option_style)
    except ValueError:
        messagebox.showerror("输入错误", "请输入有效的数字")

# Function to plot graphs for option prices and Greeks
def plot_graphs(S, K, T, r, sigma, option_type, option_style):
    spot_prices = np.linspace(0.001*S, 3 * S, 100)
    
    prices = []
    deltas = []
    vegas = []
    gammas = []
    thetas = []
    rhos = []
    
    for s in spot_prices:
        if option_style == 'vanilla':
            if option_type == 'call':
                price, _ = black_scholes(s, K, T, r, sigma)
                delta, vega, gamma, theta, rho = greeks(s, K, T, r, sigma, option_type='call')
            else:
                _, price = black_scholes(s, K, T, r, sigma)
                delta, vega, gamma, theta, rho = greeks(s, K, T, r, sigma, option_type='put')
        else:
            price = digital_option(s, K, T, r, sigma, option_type)
            delta, vega, gamma, theta, rho = digital_greeks(s, K, T, r, sigma, option_type)
        
        prices.append(price)
        deltas.append(delta)
        vegas.append(vega)
        gammas.append(gamma)
        thetas.append(theta)
        rhos.append(rho)
    
    fig, axs = plt.subplots(6, 1, figsize=(10, 30))
    
    # Plot Prices
    axs[0].plot(spot_prices, prices, label=f'{option_type.capitalize()} {option_style.capitalize()} Option Price', color='blue')
    axs[0].set_title('Price vs Spot Price')
    axs[0].set_xlabel('Spot Price')
    axs[0].set_ylabel('Price')
    axs[0].legend()
    
    # Plot Deltas
    axs[1].plot(spot_prices, deltas, label='Delta', color='green')
    axs[1].set_title('Delta vs Spot Price')
    axs[1].set_xlabel('Spot Price')
    axs[1].set_ylabel('Delta')
    axs[1].legend()
    
    # Plot Vegas
    axs[2].plot(spot_prices, vegas, label='Vega', color='purple')
    axs[2].set_title('Vega vs Spot Price')
    axs[2].set_xlabel('Spot Price')
    axs[2].set_ylabel('Vega')
    axs[2].legend()
    
    # Plot Gammas
    axs[3].plot(spot_prices, gammas, label='Gamma', color='cyan')
    axs[3].set_title('Gamma vs Spot Price')
    axs[3].set_xlabel('Spot Price')
    axs[3].set_ylabel('Gamma')
    axs[3].legend()
    
    # Plot Thetas
    axs[4].plot(spot_prices, thetas, label='Theta', color='lime')
    axs[4].set_title('Theta vs Spot Price')
    axs[4].set_xlabel('Spot Price')
    axs[4].set_ylabel('Theta')
    axs[4].legend()
    
    # Plot Rhos
    axs[5].plot(spot_prices, rhos, label='Rho', color='teal')
    axs[5].set_title('Rho vs Spot Price')
    axs[5].set_xlabel('Spot Price')
    axs[5].set_ylabel('Rho')
    axs[5].legend()
    
    plt.tight_layout()
    
    # Integrate plot into the GUI
    for widget in frame_plot.winfo_children():
        widget.destroy()
    
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Create the main window
root = tk.Tk()
root.title("期权计算器")
root.geometry("800x1000")

# Create a Notebook widget to hold different calculators
notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill="both")

# Create the Option calculator tab
frame_option = ttk.Frame(notebook)
notebook.add(frame_option, text="Option 计算器")

# Create a frame for inputs and results
frame_inputs = ttk.Frame(frame_option)
frame_inputs.grid(row=0, column=0, padx=10, pady=10, sticky=tk.N+tk.S+tk.W)

# Move all input fields and labels to frame_inputs
label_S = ttk.Label(frame_inputs, text="股票价格 (S):")
entry_S = ttk.Entry(frame_inputs)
entry_S.insert(0, "100")  # Default value

label_K = ttk.Label(frame_inputs, text="执行价格 (K):")
entry_K = ttk.Entry(frame_inputs)
entry_K.insert(0, "100")  # Default value

label_T = ttk.Label(frame_inputs, text="到期时间 (T) 年:")
entry_T = ttk.Entry(frame_inputs)
entry_T.insert(0, "1")  # Default value

label_r = ttk.Label(frame_inputs, text="无风险利率 (%) :")
entry_r = ttk.Entry(frame_inputs)
entry_r.insert(0, "5")  # Default value

label_sigma = ttk.Label(frame_inputs, text="波动率 (%) :")
entry_sigma = ttk.Entry(frame_inputs)
entry_sigma.insert(0, "20")  # Default value

var_option_type = tk.StringVar(value="call")
var_option_style = tk.StringVar(value="vanilla")

# Replace Radiobuttons with Comboboxes for Option Type
label_option_type = ttk.Label(frame_inputs, text="Option Type:")
combo_option_type = ttk.Combobox(frame_inputs, textvariable=var_option_type, state="readonly")
combo_option_type['values'] = ("call", "put")
combo_option_type.current(0)

# Replace Radiobuttons with Comboboxes for Option Style
label_option_style = ttk.Label(frame_inputs, text="Option Style:")
combo_option_style = ttk.Combobox(frame_inputs, textvariable=var_option_style, state="readonly")
combo_option_style['values'] = ("vanilla", "digital")
combo_option_style.current(0)

button_calculate = ttk.Button(frame_inputs, text="计算", command=calculate_option)

label_price = ttk.Label(frame_inputs, text="Option Price: ")
label_delta = ttk.Label(frame_inputs, text="Delta: ")
label_vega = ttk.Label(frame_inputs, text="Vega: ")
label_gamma = ttk.Label(frame_inputs, text="Gamma: ")
label_theta = ttk.Label(frame_inputs, text="Theta: ")
label_rho = ttk.Label(frame_inputs, text="Rho: ")

# Layout the input fields and labels in frame_inputs
label_S.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
entry_S.grid(row=0, column=1, padx=10, pady=5)

label_K.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
entry_K.grid(row=1, column=1, padx=10, pady=5)

label_T.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
entry_T.grid(row=2, column=1, padx=10, pady=5)

label_r.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
entry_r.grid(row=3, column=1, padx=10, pady=5)

label_sigma.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
entry_sigma.grid(row=4, column=1, padx=10, pady=5)

label_option_type.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
combo_option_type.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W)

label_option_style.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
combo_option_style.grid(row=6, column=1, padx=10, pady=5, sticky=tk.W)

button_calculate.grid(row=7, columnspan=2, pady=20)

label_price.grid(row=8, columnspan=2, pady=5)
label_delta.grid(row=9, columnspan=2, pady=5)
label_vega.grid(row=10, columnspan=2, pady=5)
label_gamma.grid(row=11, columnspan=2, pady=5)
label_theta.grid(row=12, columnspan=2, pady=5)
label_rho.grid(row=13, columnspan=2, pady=5)

# Create a frame for the plot on the right
frame_plot_container = ttk.Frame(frame_option)
frame_plot_container.grid(row=0, column=1, padx=10, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)

# Adjust frame_plot to be inside frame_plot_container
frame_plot = ttk.Frame(frame_plot_container)
frame_plot.pack(fill=tk.BOTH, expand=True)

# Configure grid weights for proper scaling
frame_option.columnconfigure(0, weight=1)
frame_option.columnconfigure(1, weight=2)
frame_option.rowconfigure(0, weight=1)

frame_plot_container.rowconfigure(0, weight=1)
frame_plot_container.columnconfigure(0, weight=1)

def on_closing():
    root.destroy()
    sys.exit(0)

# Handle window close event to properly terminate the program
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the main loop
root.mainloop()
