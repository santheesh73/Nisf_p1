import { useState } from "react";
import { Link, Navigate } from "react-router-dom";
import { UserPlus } from "lucide-react";
import Button from "../components/common/Button";
import ErrorMessage from "../components/common/ErrorMessage";
import Input from "../components/common/Input";
import { useAuth } from "../context/AuthContext";

export default function Register() {
  const { isAuthenticated, loading, register } = useAuth();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  if (!loading && isAuthenticated) {
    return <Navigate to="/generate/text" replace />;
  }

  const update = (event) => setForm((current) => ({ ...current, [event.target.name]: event.target.value }));

  const submit = async (event) => {
    event.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await register(form);
    } catch (err) {
      setError(err.message || "Unable to create account.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center px-4 py-10">
      <section className="w-full max-w-md rounded-2xl border border-slate-300/80 bg-white/82 p-6 shadow-xl shadow-slate-900/10">
        <div className="mb-6">
          <div className="text-xs font-black uppercase tracking-[0.18em] text-slate-500">NISF Text Engine</div>
          <h1 className="mt-2 text-3xl font-black text-[#343449]">Create account</h1>
        </div>
        <form className="space-y-4" onSubmit={submit}>
          <ErrorMessage message={error} />
          <Input label="Name" name="name" autoComplete="name" value={form.name} onChange={update} required />
          <Input label="Email" name="email" type="email" autoComplete="email" value={form.email} onChange={update} required />
          <Input label="Password" name="password" type="password" autoComplete="new-password" minLength={8} value={form.password} onChange={update} required />
          <Button type="submit" className="w-full" loading={submitting}>
            <UserPlus className="h-4 w-4" /> Register
          </Button>
        </form>
        <p className="mt-5 text-center text-sm text-[#64677f]">
          Already have an account?{" "}
          <Link className="font-bold text-[#343449] hover:underline" to="/login">
            Sign in
          </Link>
        </p>
      </section>
    </main>
  );
}
