import engine as eng

engine = eng.Engine()

def main():
    start_time = engine.current_time
    engine.run()
    end_time = engine.current_time
    total_time = end_time - start_time
    

if __name__ == "__main__":
    main()