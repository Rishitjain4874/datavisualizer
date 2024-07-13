import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def main():
    st.title("Histogram Example")
    
    # Generate random data for the histogram
    data = np.random.randn(1000)
    
    # Display the histogram using matplotlib
    plt.hist(data, bins=30, color='skyblue', edgecolor='black')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram')
    
    # Show plot in Streamlit
    st.pyplot()

if __name__ == "__main__":
    main()
