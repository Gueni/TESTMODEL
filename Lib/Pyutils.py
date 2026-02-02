
    def detect_mode(self, Xs):

        for var in Xs:
            if var == [[0]] or var == [0]   :    continue
            for sub in var:
                # WCA if [nom, tol] or [nom, tol, min, max]
                if len(sub) in (2, 4)       :   return "WCA"
                elif len(sub) == 1          :   return "NORMAL"

        return "NORMAL"

    def calculate_wca_values(self, iteration, Xs):
        """
        Calculate WCA values for all parameters in a given iteration.
        
        Parameters:
            iteration   (int)   : Current WCA iteration number
            Xs          (list)  : List of parameter lists for X1-X10
            
        Returns   :     (list)  : 3D list of calculated WCA values for all parameters
            
        """
        results = []

        for i, var in enumerate(Xs):
            # Unused parameter
            if var == [[0]] or var == [0]:
                results.append([0])
                continue

            wca_vals = []

            for sub in var:
                # No tolerance
                if len(sub) == 1:
                    wca_vals.append(sub[0])
                    continue

                # ---- WCA formats ----
                if len(sub) in (2, 4):
                    nom, tol = sub[0], sub[1]

                    # Default bounds if not provided
                    if len(sub) == 4:
                        mn, mx = sub[2], sub[3]
                    else:
                        mn, mx = -dp.np.inf, dp.np.inf

                    # tol <= 1  → absolute
                    # tol > 1   → relative
                    tol_type = tol <= 1

                    x = self.funtol(tol_type, iteration, i, nom, tol)

                    # Clamp
                    wca_vals.append(min(max(x, mn), mx))
                    continue

                # Fallback (should never happen, but safe)
                wca_vals.append(sub[0])

            results.append(wca_vals)

        return results

    def get_active_wca_params(self, Xs):
        """
        Identify which parameters X lists are used.
        
        Parameters  :   Xs (list): List of parameter lists for X1-X10
            
        Returns     :      (list): Indices of parameters that have WCA format
            
        """
        return [i for i, var in enumerate(Xs) if var not in [[[0]], [0]] and len(var) > 0 and isinstance(var[0], list) and len(var[0]) in (2, 4)]
