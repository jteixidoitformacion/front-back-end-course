import React from "react";
import htm from "htm";

export const html = htm.bind(React.createElement);
export const { useState, useEffect, useMemo, useCallback, useRef } = React;

const eur = new Intl.NumberFormat("es-ES", { style: "currency", currency: "EUR" });
const fecha = new Intl.DateTimeFormat("es-ES", { dateStyle: "medium" });
const fechaHora = new Intl.DateTimeFormat("es-ES", { dateStyle: "short", timeStyle: "short" });

export const formatEur = (v) => eur.format(Number(v ?? 0));
export const formatFecha = (v) => (v ? fecha.format(new Date(`${v}T00:00:00`)) : "");
export const formatFechaHora = (v) => (v ? fechaHora.format(new Date(v)) : "");
export const hoyISO = () => new Date().toISOString().slice(0, 10);
