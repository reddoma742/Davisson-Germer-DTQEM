@staticmethod
def entropy(rho):
    """
    Von Neumann entropy S = -Tr(ρ ln ρ) in natural units (nats).
    """
    # Ensure rho is Hermitian and positive semi-definite
    rho = 0.5 * (rho + rho.conj().T)
    evals = np.linalg.eigvalsh(rho)
    evals = evals[evals > 1e-15]   # ignore numerical zeros
    return -np.sum(evals * np.log(evals))
