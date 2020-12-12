import * as Yup from "yup";

const registerFormValidationRules = Yup.object().shape({
    username: Yup.string()
        .required("Το πεδίο Όνομα χρήστη είναι υποχρεωτικό.")
        .min(4, "Το Όνομα χρήστη πρέπει να αποτελείται τουλάχιστον απο 4 χαρακτήρες."),
    email: Yup.string()
        .email("Μη έγκυρο email.")
        .required("Το email είναι υποχρεωτικό.")
        .min(6, "Το email πρέπει να αποτελείται τουλάχιστον απο 6 χαρακτήρες."),
    password: Yup.string()
        .required("Το πεδίο Κωδικός είναι υποχρεωτικό.")
        .min(8, "Ο Κωδικός πρέπει να αποτελείται τουλάχιστον απο 6 χαρακτήρες."),
    first_name: Yup.string()
        .required("Το πεδίο Όνομα είναι υποχρεωτικό."),
    last_name: Yup.string()
        .required("Το πεδίο Επίθετο είναι υποχρεωτικό."),
    street_name: Yup.string()
        .required("Το πεδίο Οδός είναι υποχρεωτικό."),
    street_number: Yup.string()
        .required("Το πεδίο Αριθμός είναι υποχρεωτικό."),
    city: Yup.string()
        .required("Το πεδίο Πόλη είναι υποχρεωτικό."),
    zip_code: Yup.string()
        .required("Το πεδίο T.K είναι υποχρεωτικό.")
        .min(3, "Ο Τ.Κ πρέπει να αποτελείται τουλάχιστον από 3 ψηφία."),
    formType: Yup.string(),
    store_name: Yup.string()
        .when(
            "formType",
            {
                is: "GetStarted",
                then: s => s.required("Το πεδίο Όνομα καταστήματος είναι υποχρεωτικό.")
            }
        ),
    store_type: Yup.string()
        .when(
            "formType",
            {
                is: "GetStarted",
                then: s => s.required("Το πεδίο Είδος καταστήματος είναι υποχρεωτικό.")
            }
        ),
    company_name: Yup.string()
        .when(
            "formType",
            {
                is: "BecomeSupplier",
                then: s => s.required("Το πεδίο Όνομα εταιρίας είναι υποχρεωτικό.")
            }
        ),
    company_type: Yup.string()
        .when(
            "formType",
            {
                is: "BecomeSupplier",
                then: s => s.required("Το πεδίο Είδος εταιρίας είναι υποχρεωτικό.")
            }
        )
});

export default registerFormValidationRules;