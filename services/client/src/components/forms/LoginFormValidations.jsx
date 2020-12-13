import * as Yup from "yup";

const loginFormValidationRules = Yup.object().shape({
                    email: Yup.string()
                        .email("Μη έγκυρη διεύθυνση ηλεκτρονικού ταχυδρομείου.")
                        .required("Παρακαλώ πληκτρολογήστε το email σας."),
                    password: Yup.string()
                        .required("Παρακαλώ πληκτρολογήστε τον κωδικό πρόσβασής σας.")
                });

export default loginFormValidationRules